from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Importa apenas os routers simplificados que mantivemos
from controller.artigo_controller import artigo_router
from controller.pesquisador_controller import pesquisador_router

# Configuração básica do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="API de Busca Semântica em Currículos Lattes",
    description="Uma API para extrair e consultar dados de currículos Lattes, com funcionalidades de busca textual e semântica.",
    version="1.0.0"
)

# Configuração do CORS para permitir que o front-end acesse a API
# Em um ambiente de produção, seria bom restringir as origens.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos routers no aplicativo principal
# Apenas as rotas de pesquisador e artigo serão expostas pela API
app.include_router(pesquisador_router)
app.include_router(artigo_router)


@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raiz para verificar se a API está funcionando.
    """
    return {"message": "Bem-vindo à API de Busca em Currículos Lattes!"}

# O bloco a seguir permite rodar o app diretamente com `python main.py`
# usando o uvicorn, que é um servidor ASGI de alta performance.
if __name__ == "__main__":
    import uvicorn
    logger.info("Iniciando a aplicação com Uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=8000)