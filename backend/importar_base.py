"""
importar_base.py — lê base_conhecimento.md e grava no banco SQLite.

Uso (depois de editar o .md):   python importar_base.py
Também é chamado automaticamente pelo app.py quando o banco é criado.

Formato esperado do .md:
    ## 6. Biblioteca                      -> início de uma seção
    **6.2 Qual é o horário?**             -> uma pergunta
    texto da resposta...                  -> resposta (pode ter tabelas/listas)
    *Status: Pendente · Setor: Biblioteca*  -> fecha a entrada
Textos fora de perguntas (introduções, avisos) viram entradas do tipo "Contexto".
"""
import re
import sqlite3
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
MD_PADRAO = BASE / "base_conhecimento.md"
DB_PADRAO = BASE / "ifsc_ai.db"

RE_SECAO = re.compile(r"^## (\d+)\. (.+)$")                 # "## 6. Biblioteca"
RE_SUB = re.compile(r"^### (.+)$")                          # "### Empréstimo..."
RE_PERGUNTA = re.compile(r"^\*\*(\d+\.\d+) (.+?)\*\*$")     # "**6.2 Qual ...?**"
RE_STATUS = re.compile(r"^\*Status: ([^·*]+?)(?: · Setor: (.+?))?\*$")


def parsear(texto):
    """Devolve (regras, entradas). Cada entrada é um dicionário pronto para o banco."""
    linhas = texto.splitlines()
    entradas, regras = [], []
    secao_num, secao_nome, sub = None, "", ""
    atual = None           # entrada em construção
    n_ctx = 0              # contador de entradas de contexto na seção

    def fechar():
        nonlocal atual
        if atual:
            atual["resposta"] = "\n".join(atual["linhas"]).strip()
            if atual["resposta"]:                       # ignora entradas vazias
                entradas.append(atual)
        atual = None

    def abrir_contexto():
        nonlocal atual, n_ctx
        n_ctx += 1
        atual = dict(numero=f"{secao_num}.ctx{n_ctx}", secao=f"{secao_num}. {secao_nome}",
                     pergunta=sub or secao_nome, status="Contexto", setor=None, linhas=[])

    for ln in linhas:
        m = RE_SECAO.match(ln)
        if m:
            fechar()
            secao_num, secao_nome, sub, n_ctx = m.group(1), m.group(2).strip(), "", 0
            if secao_num != "13":                       # seção 13 = pendências internas, não vai para o agente
                abrir_contexto()
            continue
        if secao_num == "13":
            continue
        if secao_num is None:                           # antes da 1ª seção numerada: regras do agente
            regras.append(ln)
            continue
        m = RE_SUB.match(ln)
        if m:
            fechar()
            sub = m.group(1).strip()
            abrir_contexto()
            continue
        m = RE_PERGUNTA.match(ln)
        if m:
            fechar()
            atual = dict(numero=m.group(1), secao=f"{secao_num}. {secao_nome}",
                         pergunta=m.group(2).strip(), status="Base", setor=None, linhas=[])
            continue
        m = RE_STATUS.match(ln.strip())
        if m and atual and atual["status"] != "Contexto":
            atual["status"] = m.group(1).strip()
            atual["setor"] = (m.group(2) or "").strip() or None
            fechar()
            abrir_contexto()                            # o que vier depois é contexto da seção
            continue
        if atual is not None:
            atual["linhas"].append(ln)
    fechar()
    return "\n".join(regras).strip(), entradas


def importar(con, md_path=MD_PADRAO):
    """Apaga e recarrega as tabelas conhecimento, conhecimento_fts e config."""
    regras, entradas = parsear(Path(md_path).read_text(encoding="utf-8"))
    con.execute("DELETE FROM conhecimento")
    con.execute("DELETE FROM conhecimento_fts")
    for i, e in enumerate(entradas):
        cur = con.execute(
            "INSERT INTO conhecimento (ordem, numero, secao, pergunta, resposta, status, setor) "
            "VALUES (?,?,?,?,?,?,?)",
            (i, e["numero"], e["secao"], e["pergunta"], e["resposta"], e["status"], e["setor"]))
        con.execute(
            "INSERT INTO conhecimento_fts (rowid, pergunta, resposta, secao) VALUES (?,?,?,?)",
            (cur.lastrowid, e["pergunta"], e["resposta"], e["secao"]))
    con.execute("INSERT OR REPLACE INTO config (chave, valor) VALUES ('regras_agente', ?)", (regras,))
    con.commit()
    return len(entradas)


if __name__ == "__main__":
    db = Path(sys.argv[1]) if len(sys.argv) > 1 else DB_PADRAO
    con = sqlite3.connect(db)
    con.executescript((BASE / "banco.sql").read_text(encoding="utf-8").split("-- ---------- Dados iniciais")[0])
    print(importar(con), "entradas importadas em", db)
