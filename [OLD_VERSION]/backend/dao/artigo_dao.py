import logging
from typing import List, Dict, Any

from banco.conexao_db import Conexao
# A importação do modelo Artigo não é mais estritamente necessária aqui,
# mas mantê-la não causa problemas.
from model.artigo import Artigo

# Configuração do logger
logger = logging.getLogger(__name__)

class ArtigoDAO:
    """
    DAO (Data Access Object) para operações relacionadas a artigos no banco de dados.
    Versão simplificada para apenas leitura e busca textual.
    """

    def __init__(self):
        self.conexao = Conexao()

    def listar_artigos(self) -> List[Dict[str, Any]]:
        """
        Lista todos os artigos cadastrados no banco de dados.

        Returns:
            Uma lista de dicionários, onde cada dicionário representa um artigo.
        """
        query = "SELECT art_id, art_titulo, art_ano, art_doi FROM artigo ORDER BY art_ano DESC, art_titulo;"
        
        try:
            with self.conexao.conectar() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    resultados = cursor.fetchall()
            
            # Converte a lista de tuplas em uma lista de dicionários para facilitar o uso na API
            artigos = [
                {
                    "id_artigo": row[0],
                    "titulo": row[1],
                    "ano": row[2],
                    "doi": row[3]
                } for row in resultados
            ]
            return artigos

        except Exception as e:
            logger.error(f"Erro ao listar artigos: {e}")
            # Em uma aplicação real, seria bom tratar diferentes tipos de exceções.
            # Por simplicidade, estamos relançando a exceção.
            raise RuntimeError("Não foi possível listar os artigos do banco de dados.") from e

    def buscar_por_termo(self, termo: str) -> List[Dict[str, Any]]:
        """
        Busca artigos por um termo no título, de forma insensível a maiúsculas/minúsculas.

        Args:
            termo: A string a ser buscada no título dos artigos.

        Returns:
            Uma lista de dicionários com os artigos encontrados.
        """
        # A query usa ILIKE para busca case-insensitive e '%' para encontrar o termo em qualquer parte do título.
        query = "SELECT art_id, art_titulo, art_ano, art_doi FROM artigo WHERE art_titulo ILIKE %s ORDER BY art_ano DESC, art_titulo;"
        
        try:
            with self.conexao.conectar() as conn:
                with conn.cursor() as cursor:
                    # O formato com '%' deve ser passado como parâmetro para segurança (evita SQL Injection)
                    cursor.execute(query, (f'%{termo}%',))
                    resultados = cursor.fetchall()
            
            artigos_encontrados = [
                {
                    "id_artigo": row[0],
                    "titulo": row[1],
                    "ano": row[2],
                    "doi": row[3]
                } for row in resultados
            ]
            return artigos_encontrados

        except Exception as e:
            logger.error(f"Erro ao buscar artigos pelo termo '{termo}': {e}")
            raise RuntimeError(f"Não foi possível buscar os artigos pelo termo '{termo}'.") from e