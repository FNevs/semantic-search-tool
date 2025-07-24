from fastapi import APIRouter, HTTPException, status
import logging

from dao.pesquisador_dao import PesquisadorDAO

# Configuração do logger
logger = logging.getLogger(__name__)


class PesquisadorController:
    """
    Controller simplificado para operações de pesquisadores.
    Focado apenas em listar e buscar por nome.
    """
    def __init__(self):
        self.dao = PesquisadorDAO()
        self.router = APIRouter(prefix="/pesquisadores", tags=["Pesquisadores"])
        self._register_routes()

    def _register_routes(self):
        """
        Registra as rotas essenciais da API para pesquisadores.
        """
        self.router.add_api_route(
            "/",
            self.listar_todos,
            methods=["GET"],
            summary="Listar todos os pesquisadores",
            description="Retorna uma lista de todos os pesquisadores cadastrados no sistema."
        )

        self.router.add_api_route(
            "/textual/{termo_busca}",
            self.buscar_por_termo,
            methods=["GET"],
            summary="Buscar pesquisadores por nome",
            description="Retorna os pesquisadores cujo nome contém o termo de busca (insensível a maiúsculas/minúsculas)."
        )

    def listar_todos(self):
        """
        Busca e retorna todos os pesquisadores do banco de dados.
        """
        try:
            return self.dao.listar_pesquisadores()
        except Exception as e:
            logger.error(f"Erro ao listar pesquisadores: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno ao buscar pesquisadores.")

    def buscar_por_termo(self, termo_busca: str):
        """
        Busca pesquisadores que contenham o 'termo_busca' no nome.
        """
        if not termo_busca or len(termo_busca) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O termo de busca deve ter pelo menos 2 caracteres."
            )
            
        try:
            resultados = self.dao.buscar_por_termo(termo_busca)
            if not resultados:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum pesquisador encontrado para o termo fornecido.")
            
            return resultados
            
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            logger.exception(f"Erro ao buscar pesquisadores pelo termo: {termo_busca}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao processar a sua busca.")


# Instância do controller para ser importada no main.py
pesquisador_controller = PesquisadorController()
pesquisador_router = pesquisador_controller.router