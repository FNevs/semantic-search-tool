from fastapi import APIRouter, HTTPException, Query, status
import logging

from dao.artigo_dao import ArtigoDAO
# A importação do 'model.artigo' não é estritamente necessária aqui, mas pode ser mantida.

# Configuração do logger
logger = logging.getLogger(__name__)


class ArtigoController:
    """
    Controller simplificado para operações de busca de artigos.
    Focado apenas em listar e buscar por texto.
    """
    def __init__(self):
        self.dao = ArtigoDAO()
        # O router agora tem um prefixo mais genérico, já que trata apenas de artigos.
        self.router = APIRouter(prefix="/artigos", tags=["Artigos"])
        self._register_routes()

    def _register_routes(self):
        """
        Registra as rotas da API. Mantivemos apenas as rotas de leitura.
        """
        self.router.add_api_route(
            "/",
            self.listar_todos,
            methods=["GET"],
            summary="Listar todos os artigos",
            description="Retorna uma lista de todos os artigos cadastrados no banco de dados."
        )

        self.router.add_api_route(
            "/textual/{termo_busca}",
            self.buscar_por_termo,
            methods=["GET"],
            summary="Buscar artigos por termo textual",
            description="Retorna os artigos cujo título contém o termo de busca (insensível a maiúsculas/minúsculas)."
        )

    def listar_todos(self):
        """
        Busca e retorna todos os artigos do banco de dados.
        """
        try:
            return self.dao.listar_artigos()
        except Exception as e:
            logger.error(f"Erro ao listar artigos: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno ao buscar artigos.")

    def buscar_por_termo(self, termo_busca: str):
        """
        Busca artigos que contenham o 'termo_busca' no título.
        """
        if not termo_busca or len(termo_busca) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O termo de busca deve ter pelo menos 2 caracteres."
            )
        
        try:
            # A lógica de busca textual já está no DAO, então apenas a chamamos.
            resultados = self.dao.buscar_por_termo(termo_busca)
            if not resultados:
                # Retorna 404 se a busca não encontrar nada
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum artigo encontrado para o termo fornecido.")
            
            return resultados
        
        except HTTPException as http_exc:
            # Repassa a exceção HTTP (como o 404)
            raise http_exc
        except Exception as e:
            logger.exception(f"Erro ao buscar artigos pelo termo: {termo_busca}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao processar a busca.")

# Instância do controller para ser importada no main.py
artigo_controller = ArtigoController()
artigo_router = artigo_controller.router