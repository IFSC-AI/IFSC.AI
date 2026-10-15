from pathlib import Path
import os
from flask import Flask, g, jsonify
import sqlite3

BASE = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("DB_PATH", BASE / "ifsc_ai.db"))
FRONTEND = BASE.parent / "frontend"
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "admin123")
N8N_URL = os.environ.get("N8N_URL", "").strip()

app = Flask(__name__, static_folder=None)

# Parte 1 - Banco de Dados ---------------------------------------------

def get_db():
    # essa função devolve a conexão com o Banco, criando uma só vez por requisição
    if "db" not in g: #se ainda não estiver aberto conexão na requisição
        g.db = sqlite3.connect(DB_PATH) #abre o arquivo do banco
        g.db.row_factory = sqlite3.Row #permite acessar4 colunas pelo nome, assim: linha['nome']
    return g.db
        
@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()
        
def init_db():
    if DB_PATH.exists():
        return
    con = sqlite3.connect(DB_PATH)
    con.executescript((BASE / "banco.sql").read_text(encoding="utf-8"))
    con.commit()
    con.close()
    
def rows(cur):
    return [dict(r) for r in cur.fetchall(s)]



# Parte 2 - Rotas de Admin ----------------------------------------------
@app.post("/api/conversas")
@admin_required
def registrar_conversa():
    #função serve para o n8n chamar essa rota para assim registrar o que chega do wpp
    d = request.get_json(silent=True) or {}
    if not d.get("pergunta"): #trata um possivel erro caso não haja pergunta
        return jsonify(erro="campo 'pergunta' obrigatório"), 400
    registrar(get_db(), d.get("origem", "whatsapp"), d["pergunta"],
            d.get("resposta"), d.get("encontrou", True))
    return jsonify(ok = True), 201

# faltou terminar essa parte, faltam os comando sql


# Parte 3 - Rotas Públicas



# Parte 4 - Utilidades



# Parte 5 - Integração com Frontend