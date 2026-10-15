from pathlib import Path
import os
from flask import Flask, g
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