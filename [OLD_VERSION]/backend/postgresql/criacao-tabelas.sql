-- Remove tabelas existentes, se houver, para garantir um ambiente limpo.
-- CUIDADO: Isso apaga todos os dados. Use apenas em ambiente de desenvolvimento.
DROP TABLE IF EXISTS artigo, pesquisador CASCADE;

-- Habilita a extensão pgvector. Vamos mantê-la para facilitar a reintrodução da busca semântica no futuro.
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabela para armazenar os dados do pesquisador.
CREATE TABLE pesquisador (
    pes_id SERIAL PRIMARY KEY,
    pes_nome VARCHAR(255) NOT NULL,
    pes_resumo TEXT,
    pes_lattes_id VARCHAR(50) UNIQUE NOT NULL
);

-- Tabela para armazenar os artigos publicados pelo pesquisador.
CREATE TABLE artigo (
    art_id SERIAL PRIMARY KEY,
    art_pes_id INT NOT NULL,
    art_titulo TEXT NOT NULL,
    art_ano INT,
    art_doi VARCHAR(100),
    CONSTRAINT fk_pesquisador
        FOREIGN KEY(art_pes_id)
        REFERENCES pesquisador(pes_id)
);

-- Cria um índice para otimizar a busca textual por título.
CREATE INDEX idx_artigo_titulo ON artigo USING gin(to_tsvector('portuguese', art_titulo));

-- Comentários para clareza
COMMENT ON TABLE pesquisador IS 'Armazena os dados cadastrais dos pesquisadores extraídos do Lattes.';
COMMENT ON TABLE artigo IS 'Armazena as informações sobre os artigos publicados pelos pesquisadores.';