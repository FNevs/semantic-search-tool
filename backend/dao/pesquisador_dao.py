import logging
from typing import List, Dict, Any

from banco.conexao_db import Conexao
# A importação do modelo 'Pesquisador' não é estritamente necessária aqui.
from model.pesquisador import Pesquisador

# Configuração do logger
logger = logging.getLogger(__name__)

class PesquisadorDAO:
    """
    DAO (Data Access Object) para operações relacionadas a pesquisadores.
    Versão simplificada para apenas leitura e busca textual.
    """

    def __init__(self):
        self.conexao = Conexao()

    def listar_pesquisadores(self) -> List[Dict[str, Any]]:
        """
        Lista todos os pesquisadores cadastrados no banco de dados.

        Returns:
            Uma lista de dicionários, onde cada dicionário representa um pesquisador.
        """
        query = "SELECT pes_id, pes_nome, pes_resumo, pes_lattes_id FROM pesquisador ORDER BY pes_nome;"
        
        try:
            with self.conexao.conectar() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    resultados = cursor.fetchall()
            
            pesquisadores = [
                {
                    "id_pesquisador": row[0],
                    "nome": row[1],
                    "resumo": row[2],
                    "lattes_id": row[3]
                } for row in resultados
            ]
            return pesquisadores

        except Exception as e:
            logger.error(f"Erro ao listar pesquisadores: {e}")
            raise RuntimeError("Não foi possível listar os pesquisadores do banco de dados.") from e

    def buscar_por_termo(self, termo: str) -> List[Dict[str, Any]]:
        """
        Busca pesquisadores por um termo no nome, de forma insensível a maiúsculas/minúsculas.

        Args:
            termo: A string a ser buscada no nome dos pesquisadores.

        Returns:
            Uma lista de dicionários com os pesquisadores encontrados.
        """
        query = "SELECT pes_id, pes_nome, pes_resumo, pes_lattes_id FROM pesquisador WHERE pes_nome ILIKE %s ORDER BY pes_nome;"
        
        try:
            with self.conexao.conectar() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (f'%{termo}%',))
                    resultados = cursor.fetchall()
            
            pesquisadores_encontrados = [
                {
                    "id_pesquisador": row[0],
                    "nome": row[1],
                    "resumo": row[2],
                    "lattes_id": row[3]
                } for row in resultados
            ]
            return pesquisadores_encontrados

        except Exception as e:
            logger.error(f"Erro ao buscar pesquisadores pelo termo '{termo}': {e}")
            raise RuntimeError(f"Não foi possível buscar os pesquisadores pelo termo '{termo}'.") from e