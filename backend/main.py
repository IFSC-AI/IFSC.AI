import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client


# Carrega as variáveis do .env na raiz do projeto
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ_PROJETO / ".env")


# Obtém as configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Configure SUPABASE_URL e SUPABASE_KEY no arquivo .env."
    )


# Cria a conexão com o Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# Cria a aplicação FastAPI
app = FastAPI(
    title="IFSC.AI API",
    description="API de conteúdos do site IFSC.AI",
    version="1.0.0"
)


# Permite a comunicação com o frontend durante o desenvolvimento
origens_permitidas = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:5501",
    "http://127.0.0.1:5501"
]

FRONTEND_URL = os.getenv("FRONTEND_URL")

if FRONTEND_URL:
    origens_permitidas.append(FRONTEND_URL.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"]
)


# Rota inicial
@app.get("/")
def home():
    return {
        "projeto": "IFSC.AI",
        "status": "API funcionando"
    }


# Retorna todos os conteúdos do Supabase
@app.get("/api/conteudos")
def listar_conteudos():
    try:
        resposta = (
            supabase
            .table("conteudos")
            .select("id, created_at, chave, titulo, descricao, url")
            .order("id")
            .execute()
        )

        return resposta.data

    except Exception as erro:
        print("Erro ao consultar conteúdos:", erro)

        raise HTTPException(
            status_code=500,
            detail="Não foi possível consultar os conteúdos."
        )


# Retorna um conteúdo específico pela chave
@app.get("/api/conteudos/{chave}")
def buscar_conteudo(chave: str):
    try:
        resposta = (
            supabase
            .table("conteudos")
            .select("id, created_at, chave, titulo, descricao, url")
            .eq("chave", chave)
            .limit(1)
            .execute()
        )

        if not resposta.data:
            raise HTTPException(
                status_code=404,
                detail="Conteúdo não encontrado."
            )

        return resposta.data[0]

    except HTTPException:
        raise

    except Exception as erro:
        print("Erro ao buscar conteúdo:", erro)

        raise HTTPException(
            status_code=500,
            detail="Não foi possível consultar o conteúdo."
        )