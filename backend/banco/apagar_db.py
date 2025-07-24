import logging
from conexao_db import Conexao

# Configuração do logger
logger = logging.getLogger(__name__)

def apagar_tabelas():
    """
    Função para apagar as tabelas 'artigo' e 'pesquisador' do banco de dados.
    Útil para limpar o ambiente de desenvolvimento antes de uma nova carga de dados.
    """
    # Lista das tabelas a serem apagadas. A ordem é importante por causa das chaves estrangeiras.
    # 'artigo' deve ser apagada antes de 'pesquisador'.
    tabelas = ["artigo", "pesquisador"]
    
    try:
        # Cria uma nova instância da classe Conexao
        conexao = Conexao()
        with conexao.conectar() as conn:
            with conn.cursor() as cursor:
                for tabela in tabelas:
                    logger.info(f"Apagando a tabela: {tabela}...")
                    # O comando CASCADE remove a tabela e quaisquer objetos dependentes (como chaves estrangeiras)
                    cursor.execute(f"DROP TABLE IF EXISTS {tabela} CASCADE;")
                
                # Confirma as alterações no banco de dados
                conn.commit()
                logger.info("Tabelas apagadas com sucesso!")

    except Exception as e:
        logger.error(f"Ocorreu um erro ao tentar apagar as tabelas: {e}")
        # Desfaz quaisquer alterações se ocorrer um erro
        if 'conn' in locals() and conn:
            conn.rollback()

if __name__ == "__main__":
    # Executa a função quando o script é chamado diretamente
    apagar_tabelas()