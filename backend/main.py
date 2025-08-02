from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import xml.etree.ElementTree as ET
from typing import List
import os

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
def init_db():
    conn = sqlite3.connect('lattes.db')
    cursor = conn.cursor()
    
    # Create researchers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS researchers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL UNIQUE
    )
    ''')
    
    # Create publications table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS publications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        researcher_id INTEGER,
        FOREIGN KEY (researcher_id) REFERENCES researchers (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Initialize the database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Function to parse XML and extract data
def parse_lattes_xml(xml_content):
    root = ET.fromstring(xml_content)
    
    # Extract researcher's full name from DADOS-GERAIS
    dados_gerais = root.find('.//DADOS-GERAIS')
    if dados_gerais is None:
        return None, []
    
    full_name = dados_gerais.get('NOME-COMPLETO')
    
    # Extract publication titles from PRODUCAO-BIBLIOGRAFICA
    publications = []
    producao_bibliografica = root.find('.//PRODUCAO-BIBLIOGRAFICA')
    
    if producao_bibliografica is not None:
        # Look for articles
        for artigo in producao_bibliografica.findall('.//ARTIGO-PUBLICADO'):
            dados_basicos = artigo.find('.//DADOS-BASICOS-DO-ARTIGO')
            if dados_basicos is not None and dados_basicos.get('TITULO-DO-ARTIGO'):
                publications.append(dados_basicos.get('TITULO-DO-ARTIGO'))
        
        # Look for books
        for livro in producao_bibliografica.findall('.//LIVRO-PUBLICADO-OU-ORGANIZADO'):
            dados_basicos = livro.find('.//DADOS-BASICOS-DO-LIVRO')
            if dados_basicos is not None and dados_basicos.get('TITULO-DO-LIVRO'):
                publications.append(dados_basicos.get('TITULO-DO-LIVRO'))
        
        # Look for book chapters
        for capitulo in producao_bibliografica.findall('.//CAPITULO-DE-LIVRO-PUBLICADO'):
            dados_basicos = capitulo.find('.//DADOS-BASICOS-DO-CAPITULO')
            if dados_basicos is not None and dados_basicos.get('TITULO-DO-CAPITULO-DO-LIVRO'):
                publications.append(dados_basicos.get('TITULO-DO-CAPITULO-DO-LIVRO'))
        
        # Look for conference papers
        for trabalho in producao_bibliografica.findall('.//TRABALHO-EM-EVENTOS'):
            dados_basicos = trabalho.find('.//DADOS-BASICOS-DO-TRABALHO')
            if dados_basicos is not None and dados_basicos.get('TITULO-DO-TRABALHO'):
                publications.append(dados_basicos.get('TITULO-DO-TRABALHO'))
    
    return full_name, publications

# Endpoint to process XML files
@app.post("/process-xmls")
async def process_xmls(files: List[UploadFile] = File(...)):
    conn = sqlite3.connect('lattes.db')
    cursor = conn.cursor()
    
    processed_count = 0
    researchers_count = 0
    publications_count = 0
    
    for file in files:
        if not file.filename.endswith('.xml'):
            continue
        
        content = await file.read()
        full_name, publications = parse_lattes_xml(content)
        
        if full_name and publications:
            # Insert or get researcher
            cursor.execute("SELECT id FROM researchers WHERE full_name = ?", (full_name,))
            researcher = cursor.fetchone()
            
            if researcher is None:
                cursor.execute("INSERT INTO researchers (full_name) VALUES (?)", (full_name,))
                researcher_id = cursor.lastrowid
                researchers_count += 1
            else:
                researcher_id = researcher[0]
            
            # Insert publications
            for title in publications:
                cursor.execute("INSERT INTO publications (title, researcher_id) VALUES (?, ?)", 
                              (title, researcher_id))
                publications_count += 1
            
            processed_count += 1
    
    conn.commit()
    conn.close()
    
    return {
        "message": f"Successfully processed {processed_count} XML files",
        "researchers_added": researchers_count,
        "publications_added": publications_count
    }

# Endpoint to search for publications
@app.get("/search")
async def search_publications(query: str = Query(...)):
    conn = sqlite3.connect('lattes.db')
    cursor = conn.cursor()
    
    # Search for publications with titles containing the query (case-insensitive)
    cursor.execute("""
    SELECT p.title, r.full_name 
    FROM publications p 
    JOIN researchers r ON p.researcher_id = r.id 
    WHERE LOWER(p.title) LIKE LOWER(?)
    """, (f'%{query}%',))
    
    results = []
    for row in cursor.fetchall():
        results.append({
            "title": row[0],
            "researcher": row[1]
        })
    
    conn.close()
    
    return results

# Root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Lattes XML Processor API is running"}

# Run the application with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)