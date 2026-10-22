"""
IFSC.AI — backend de demonstração (Flask + SQLite)

Rodar:
    pip install -r requirements.txt
    python app.py          ->  http://localhost:5000
"""
import json
import os
import re
import sqlite3
import unicodedata
import urllib.error
import urllib.request
from functools import wraps
from pathlib import Path

from flask import Flask, g, jsonify, request, send_from_directory

from importar_base import importar

# Configurações: caminhos, token de admin e endereço do webhook do n8n.
BASE = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("DB_PATH", BASE / "ifsc_ai.db"))
FRONTEND = BASE.parent / "frontend"
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "admin123")
N8N_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "").strip()

app = Flask(__name__, static_folder=None)



# Parte 1 - Banco de Dados


def get_db():
    """Devolve a conexão com o banco, criando uma só por requisição."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Cria as tabelas, carrega os dados iniciais e importa o base_conhecimento.md."""
    novo = not DB_PATH.exists()
    con = sqlite3.connect(DB_PATH)
    sql = (BASE / "banco.sql").read_text(encoding="utf-8")
    esquema, _, seed = sql.partition("-- ---------- Dados iniciais")
    con.executescript(esquema)
    if novo:
        con.executescript(seed)
    if con.execute("SELECT COUNT(*) FROM conhecimento").fetchone()[0] == 0:
        importar(con)
    con.commit()
    con.close()


def rows(cur):
    """Converte o resultado de uma consulta em lista de dicionários."""
    return [dict(r) for r in cur.fetchall()]


# Parte 2 - UTILIDADES

def admin_required(fn):
    """Decorador: só deixa a rota executar se o cabeçalho X-Admin-Token estiver correto."""
    @wraps(fn)
    def wrapper(*a, **kw):
        if request.headers.get("X-Admin-Token") != ADMIN_TOKEN:
            return jsonify(erro="não autorizado"), 401
        return fn(*a, **kw)
    return wrapper


def normalizar(txt):
    """Deixa o texto em minúsculas e sem acentos."""
    txt = unicodedata.normalize("NFD", (txt or "").lower())
    return "".join(c for c in txt if unicodedata.category(c) != "Mn")


# Palavras comuns que não ajudam a encontrar nada na busca.
STOPWORDS = set(
    "a o as os um uma de do da dos das em no na nos nas por para com e ou que qual quais "
    "onde como quando fica ficam eu posso quero preciso tem ter ha sao e esta estao me "
    "quanto quantos quantas quantidade".split()
)


def tokens(txt):
    """Quebra um texto em um conjunto de palavras úteis (sem acento, sem stopwords)."""
    return {t for t in re.findall(r"[a-z0-9]+", normalizar(txt))
            if t not in STOPWORDS and len(t) > 2}


def buscar_setores(db, consulta, limite=5):
    """Busca setores por pontos: nome vale 3, palavras-chave 2, descrição e bloco 1."""
    qt = tokens(consulta)
    if not qt:
        return []
    resultados = []
    for s in rows(db.execute("SELECT * FROM setores")):
        pontos = (len(qt & tokens(s["nome"])) * 3
                  + len(qt & tokens(s["palavras_chave"])) * 2
                  + len(qt & tokens(f'{s["descricao"]} {s["bloco"]}')))
        if pontos:
            resultados.append((pontos, s))
    resultados.sort(key=lambda x: -x[0])
    return [s for _, s in resultados[:limite]]


# Parte 3 - Base de Conhecimento (importada do .md)


MSG_NAO_CONSTA = ("Essa informação não consta na minha base. "
                  "Procure o DAE (Bloco A), que faz o atendimento geral aos estudantes.")


def radical(t):
    """Aproxima o radical da palavra: tira o plural e, em palavras longas, as 2 últimas letras."""
    if t.endswith("s") and len(t) > 4:
        t = t[:-1]
    return t[:-2] if len(t) >= 8 else t


# Palavras que o usuário usa e a base escreve de outro jeito.
# Cada grupo é satisfeito por qualquer uma das alternativas.
SINONIMOS = {
    "pedir": ["solicit"], "pedido": ["solicit"], "requerer": ["solicit"],
    "horas": ["hora", "carga"], "disciplinas": ["disciplina", "unidade", "componente"],
    "restaurante": ["restaurante", "refeitorio", "cantina"],
    "comer": ["aliment", "lanche", "cantina"],
}


def termos_fts(pergunta):
    """Transforma a pergunta em uma lista de grupos de radicais para a busca."""
    grupos = []
    for t in sorted(tokens(pergunta)):
        grupo = SINONIMOS.get(t) or [radical(t)]
        if grupo not in grupos:
            grupos.append(grupo)
    return grupos


def buscar_conhecimento(db, pergunta, limite=5):
    """
    Busca na base por relevância (bm25 do FTS5).
    Em seguida descarta os resultados que não contêm palavras suficientes da pergunta
    e ordena por cobertura, semelhança com a pergunta da base e relevância.
    """
    grupos = termos_fts(pergunta)
    if not grupos:
        return []
    alternativas = sorted({alt for g in grupos for alt in g})
    try:
        cand = db.execute(
            "SELECT c.*, bm25(conhecimento_fts, 4.0, 1.0, 0.5) AS rel "
            "FROM conhecimento_fts JOIN conhecimento c ON c.id = conhecimento_fts.rowid "
            "WHERE conhecimento_fts MATCH ? ORDER BY rel LIMIT 25",
            (" OR ".join(a + "*" for a in alternativas),)).fetchall()
    except sqlite3.OperationalError:
        return []

    n = len(grupos)
    minimo = 1.0 if n <= 2 else (0.67 if n == 3 else 0.5)
    palavras_q = tokens(pergunta)
    achados = []
    for r in cand:
        palavras = set(re.findall(r"[a-z0-9]+", normalizar(f'{r["pergunta"]} {r["resposta"]}')))
        ok = sum(1 for g in grupos if any(p.startswith(a) for a in g for p in palavras))
        cobertura = ok / n
        if cobertura < minimo:
            continue
        pw = tokens(r["pergunta"])
        parecida = len(palavras_q & pw) / len(pw) if pw else 0
        achados.append((-cobertura, -parecida, r["status"] == "Contexto", r["rel"], dict(r)))
    achados.sort(key=lambda x: x[:4])
    return [a[4] for a in achados[:limite]]


def limpar_md(txt, maximo=1800):
    """Converte markdown em texto simples: remove negrito, ajeita links e tabelas e corta textos longos."""
    linhas = []
    for ln in txt.splitlines():
        if re.match(r"^\|\s*-+", ln):
            continue
        if ln.startswith("|"):
            ln = " — ".join(c.strip() for c in ln.strip("|").split("|") if c.strip())
        linhas.append(ln)
    out = "\n".join(linhas).replace("**", "")
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", out)
    if len(out) > maximo:
        out = out[:maximo].rsplit("\n", 1)[0] + "\n[…] Resposta completa: confira com a coordenação ou o PPC."
    return out.strip()


def resposta_conhecimento(item):
    """Monta a resposta final de acordo com o status da entrada (Base, Relato, Pendente ou PPC)."""
    texto = limpar_md(item["resposta"])
    setor = item["setor"] or "o setor responsável"
    st = item["status"]
    if st == "Relato":
        return f"{texto}\n\nObs.: informação baseada em relato de servidor e pode mudar; confirme com {setor}."
    if st == "Pendente":
        return ("Ainda não há confirmação oficial sobre isso. O que consta na base:\n"
                f"{texto}\n\nConfirme com {item['setor'] or 'o DAE'}.")
    if st == "PPC":
        return f"{texto}\n\nFonte: PPC oficial do curso; confira a versão vigente com a coordenação."
    return texto


# Parte 4 - n8n E REGISTRO DE CONVERSAS


def perguntar_n8n(pergunta):
    """Envia a pergunta ao webhook do n8n e devolve o texto da resposta."""
    req = urllib.request.Request(
        N8N_WEBHOOK_URL,
        data=json.dumps({"pergunta": pergunta, "origem": "site"}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        corpo = r.read().decode("utf-8", "replace")
    # O n8n pode devolver JSON (objeto ou lista) ou texto puro; tentamos extrair o texto.
    try:
        dados = json.loads(corpo)
        if isinstance(dados, list) and dados:
            dados = dados[0]
        if isinstance(dados, dict):
            return dados.get("resposta") or dados.get("output") or dados.get("text") or corpo
    except ValueError:
        pass
    return corpo


def registrar(db, origem, pergunta, resposta, encontrou):
    """Grava a conversa na tabela 'conversas', que alimenta as estatísticas."""
    db.execute(
        "INSERT INTO conversas (origem, pergunta, resposta, encontrou) VALUES (?,?,?,?)",
        (origem, pergunta, resposta, 1 if encontrou else 0),
    )
    db.commit()


# Parte 5 - Rotas Públicas

@app.get("/api/health")
def health():
    return jsonify(status="ok", n8n_configurado=bool(N8N_WEBHOOK_URL))


@app.get("/api/setores")
def listar_setores():
    db = get_db()
    q = request.args.get("q", "").strip()
    if q:
        return jsonify(buscar_setores(db, q, 20))
    return jsonify(rows(db.execute("SELECT * FROM setores ORDER BY nome")))


@app.get("/api/setores/<int:sid>")
def obter_setor(sid):
    r = get_db().execute("SELECT * FROM setores WHERE id=?", (sid,)).fetchone()
    return (jsonify(dict(r)), 200) if r else (jsonify(erro="não encontrado"), 404)


@app.get("/api/faq")
def listar_faq():
    return jsonify(rows(get_db().execute(
        "SELECT id, pergunta, resposta FROM faq WHERE ativo=1 ORDER BY ordem, id")))


@app.post("/api/chat")
def chat():
    """
    Recebe {"pergunta": "..."} e responde.
    Ordem: 1) n8n, se estiver configurado; 2) base de conhecimento local;
    3) mensagem "não consta na base". Toda pergunta é registrada no log.
    """
    dados = request.get_json(silent=True) or {}
    pergunta = (dados.get("pergunta") or "").strip()
    if not pergunta:
        return jsonify(erro="envie o campo 'pergunta'"), 400
    if len(pergunta) > 500:
        return jsonify(erro="pergunta muito longa (máx. 500 caracteres)"), 400

    db = get_db()
    fonte, resposta, meta = "base-local", None, {}
    if N8N_WEBHOOK_URL:
        try:
            resposta, fonte = perguntar_n8n(pergunta), "n8n"
        except (urllib.error.URLError, TimeoutError, OSError):
            resposta = None
    if not resposta:
        fonte = "base-local"
        achados = buscar_conhecimento(db, pergunta, 1)
        if achados:
            resposta = resposta_conhecimento(achados[0])
            meta = dict(numero=achados[0]["numero"], status=achados[0]["status"])

    encontrou = resposta is not None
    if not encontrou:
        resposta = MSG_NAO_CONSTA
    registrar(db, "site", pergunta, resposta, encontrou)
    return jsonify(resposta=resposta, fonte=fonte, encontrou=encontrou, **meta)


@app.get("/api/conhecimento")
def api_conhecimento():
    """Sem 'q': lista as entradas da base. Com 'q': devolve as melhores respostas (usado pelo n8n)."""
    db = get_db()
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify(rows(db.execute(
            "SELECT numero, secao, pergunta, status, setor FROM conhecimento ORDER BY ordem")))
    return jsonify([{k: r[k] for k in ("numero", "secao", "pergunta", "resposta", "status", "setor")}
                    for r in buscar_conhecimento(db, q, int(request.args.get("limite", 5)))])


@app.get("/api/regras")
def api_regras():
    """Devolve as regras de comportamento do agente (úteis como prompt de sistema no n8n)."""
    r = get_db().execute("SELECT valor FROM config WHERE chave='regras_agente'").fetchone()
    return jsonify(regras=r["valor"] if r else "")


@app.post("/api/feedback")
def enviar_feedback():
    """Valida a nota (1 a 5) e grava a avaliação do usuário."""
    dados = request.get_json(silent=True) or {}
    try:
        nota = int(dados.get("nota"))
    except (TypeError, ValueError):
        return jsonify(erro="nota deve ser um número de 1 a 5"), 400
    if not 1 <= nota <= 5:
        return jsonify(erro="nota deve ser de 1 a 5"), 400
    comentario = (dados.get("comentario") or "").strip()[:1000]
    db = get_db()
    db.execute("INSERT INTO feedback (nota, comentario) VALUES (?,?)", (nota, comentario))
    db.commit()
    return jsonify(ok=True), 201


# Parte 6 - Rotas de Admin (exigem o cabeçalho X-Admin-Token)


@app.post("/api/conversas")
@admin_required
def registrar_conversa():
    """O n8n chama esta rota para registrar as conversas que chegaram pelo WhatsApp."""
    d = request.get_json(silent=True) or {}
    if not d.get("pergunta"):
        return jsonify(erro="campo 'pergunta' obrigatório"), 400
    registrar(get_db(), d.get("origem", "whatsapp"), d["pergunta"],
              d.get("resposta"), d.get("encontrou", True))
    return jsonify(ok=True), 201


@app.get("/api/stats")
@admin_required
def stats():
    """Estatísticas: totais, perguntas sem resposta, nota média e últimos feedbacks."""
    db = get_db()
    um = lambda sql: db.execute(sql).fetchone()[0]
    return jsonify(
        total_perguntas=um("SELECT COUNT(*) FROM conversas"),
        sem_resposta=um("SELECT COUNT(*) FROM conversas WHERE encontrou=0"),
        nota_media=round(um("SELECT COALESCE(AVG(nota),0) FROM feedback"), 2),
        total_feedbacks=um("SELECT COUNT(*) FROM feedback"),
        por_dia=rows(db.execute(
            "SELECT date(criado_em) AS dia, COUNT(*) AS total FROM conversas "
            "GROUP BY dia ORDER BY dia DESC LIMIT 14")),
        por_origem=rows(db.execute(
            "SELECT origem, COUNT(*) AS total FROM conversas GROUP BY origem")),
        perguntas_sem_resposta=rows(db.execute(
            "SELECT pergunta, criado_em FROM conversas WHERE encontrou=0 "
            "ORDER BY id DESC LIMIT 20")),
        ultimos_feedbacks=rows(db.execute(
            "SELECT nota, comentario, criado_em FROM feedback ORDER BY id DESC LIMIT 10")),
    )


# Colunas permitidas ao criar ou editar um setor.
CAMPOS_SETOR = ("nome", "bloco", "descricao", "horario", "contato", "palavras_chave")


@app.post("/api/setores")
@admin_required
def criar_setor():
    d = request.get_json(silent=True) or {}
    if not d.get("nome"):
        return jsonify(erro="campo 'nome' obrigatório"), 400
    db = get_db()
    cur = db.execute(
        f"INSERT INTO setores ({','.join(CAMPOS_SETOR)}) "
        f"VALUES ({','.join('?' * len(CAMPOS_SETOR))})",
        [d.get(c) for c in CAMPOS_SETOR])
    db.commit()
    return jsonify(id=cur.lastrowid), 201


@app.put("/api/setores/<int:sid>")
@admin_required
def editar_setor(sid):
    """Atualiza só os campos enviados no pedido."""
    d = request.get_json(silent=True) or {}
    campos = [c for c in CAMPOS_SETOR if c in d]
    if not campos:
        return jsonify(erro="nada para atualizar"), 400
    db = get_db()
    cur = db.execute(
        f"UPDATE setores SET {','.join(c + '=?' for c in campos)} WHERE id=?",
        [d[c] for c in campos] + [sid])
    db.commit()
    return (jsonify(ok=True), 200) if cur.rowcount else (jsonify(erro="não encontrado"), 404)


@app.delete("/api/setores/<int:sid>")
@admin_required
def apagar_setor(sid):
    db = get_db()
    cur = db.execute("DELETE FROM setores WHERE id=?", (sid,))
    db.commit()
    return (jsonify(ok=True), 200) if cur.rowcount else (jsonify(erro="não encontrado"), 404)



# Parte 7 - Frontend (o mesmo servidor entrega o site)

@app.get("/")
def index():
    return send_from_directory(FRONTEND, "index.html")


@app.get("/<path:nome>")
def estaticos(nome):
    return send_from_directory(FRONTEND, nome)


init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)