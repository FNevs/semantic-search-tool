import pandas as pd
import logging
from conexao_db import Conexao

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def povoar_banco_de_dados():
    """
    Popula as tabelas 'pesquisador' e 'artigo' a partir de um arquivo CSV.
    Assume que o CSV 'lattes_data.csv' existe no mesmo diretório.
    """
    try:
        # Carrega os dados do CSV para um DataFrame do pandas
        df = pd.read_csv('lattes_data.csv')
        logger.info("Arquivo CSV 'lattes_data.csv' carregado com sucesso.")
    except FileNotFoundError:
        logger.error("Erro: O arquivo 'lattes_data.csv' não foi encontrado.")
        logger.error("Por favor, execute o notebook de pré-processamento para gerá-lo primeiro.")
        return
    except Exception as e:
        logger.error(f"Erro ao ler o arquivo CSV: {e}")
        return

    conexao = Conexao()
    with conexao.conectar() as conn:
        with conn.cursor() as cursor:
            try:
                # --- Povoar a tabela 'pesquisador' ---
                logger.info("Povoando a tabela 'pesquisador'...")
                # Seleciona dados únicos de pesquisadores e remove duplicatas
                df_pesquisadores = df[['pes_nome', 'pes_resumo', 'pes_lattes_id']].drop_duplicates().dropna(subset=['pes_lattes_id'])

                for _, row in df_pesquisadores.iterrows():
                    # Insere o pesquisador e ignora se o lattes_id já existir
                    cursor.execute(
                        """
                        INSERT INTO pesquisador (pes_nome, pes_resumo, pes_lattes_id)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (pes_lattes_id) DO NOTHING;
                        """,
                        (row['pes_nome'], row['pes_resumo'], str(row['pes_lattes_id']))
                    )
                logger.info(f"{len(df_pesquisadores)} registros de pesquisadores processados.")

                # --- Povoar a tabela 'artigo' ---
                logger.info("Povoando a tabela 'artigo'...")
                # Filtra as linhas que correspondem a artigos e têm título
                df_artigos = df[df['tipo'] == 'artigo'].dropna(subset=['titulo'])

                for _, row in df_artigos.iterrows():
                    # Primeiro, busca o ID do pesquisador correspondente
                    cursor.execute("SELECT pes_id FROM pesquisador WHERE pes_lattes_id = %s;", (str(row['pes_lattes_id']),))
                    resultado = cursor.fetchone()
                    
                    if resultado:
                        pes_id = resultado[0]
                        # Insere o artigo com a chave estrangeira correta
                        cursor.execute(
                            """
                            INSERT INTO artigo (art_pes_id, art_titulo, art_ano, art_doi)
                            VALUES (%s, %s, %s, %s);
                            """,
                            (pes_id, row['titulo'], int(row['ano']), row['doi'])
                        )
                logger.info(f"{len(df_artigos)} registros de artigos processados.")

                # Confirma todas as transações
                conn.commit()
                logger.info("Povoamento do banco de dados concluído com sucesso!")

            except Exception as e:
                logger.error(f"Erro durante o povoamento do banco de dados: {e}")
                # Desfaz as alterações em caso de erro
                conn.rollback()

if __name__ == "__main__":
    povoar_banco_de_dados()