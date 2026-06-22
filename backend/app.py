"""
Ponto de entrada da aplicação FastAPI.

API de Extração de Paleta de Cores - recebe uma imagem, identifica
as cores predominantes utilizando K-Means e retorna a imagem com a
paleta anexada (e/ou os dados da paleta em JSON).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from backend.routes.image_routes import router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="API de Extração de Paleta de Cores",
    description=(
        "Recebe uma imagem, identifica as principais cores utilizando "
        "K-Means e retorna a imagem com a paleta anexada e/ou os dados "
        "da paleta em formato JSON."
    ),
    version="1.0.0",
)

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router, prefix="/api", tags=["Paleta de Cores"])


@app.get("/health", tags=["Status"])
def health_check():
    """Endpoint simples para verificar se a API está rodando."""
    return {"status": "ok"}


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
