from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
import os

from .load_json import carregar_dados_json
from .config import (
    DATA_DIR, DATA_JSON, PDF_URL, PDF_FILE
)
from .utils import inicializar_dados, garantir_diretorio
from .models import TrabalhoAcademico, MensagemResposta, ListaTrabalhos, EstatisticasGerais

# Inicialização da aplicação
garantir_diretorio(DATA_DIR)

if not os.path.exists(DATA_JSON):
    inicializar_dados(PDF_URL, PDF_FILE, DATA_JSON)


app = FastAPI(
    title="API Mostra Científica IFRS Restinga",
    description="API para consulta dos trabalhos da 13ª Mostra Científica do IFRS – Campus Restinga",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/", response_model=MensagemResposta, tags=["Informações"])
def read_root():
    """
    Endpoint raiz da API
    
    Retorna uma mensagem de boas-vindas com informações sobre a API.
    """
    return {"mensagem": "API para os dados da 13ª Mostra Científica do IFRS – Campus Restinga"}

@app.get("/anais2024", response_model=List[TrabalhoAcademico], tags=["Trabalhos Acadêmicos"])
def get_anais(
    termo_titulo: Optional[str] = Query(None, description="Termo para busca no título dos trabalhos"),
    autor: Optional[str] = Query(None, description="Nome do autor para busca nos trabalhos"),
    palavra_chave: Optional[str] = Query(None, description="Palavra-chave para busca nos trabalhos")
):
    """
    Retorna todos os trabalhos dos anais de 2024
    
    Permite filtrar os trabalhos por:
    - **termo_titulo**: Busca por termo no título do trabalho
    - **autor**: Busca por nome do autor
    - **palavra_chave**: Busca por palavra-chave
    
    Se nenhum filtro for aplicado, retorna todos os trabalhos.
    """
    try:
        dados = carregar_dados_json(DATA_JSON)
        dados_filtrados = dados

        def filtrar(campo, valor, lista):
            return list(filter(lambda trabalho: valor.lower() in str(trabalho[campo]).lower(), lista))

        if termo_titulo:
            dados_filtrados = filtrar("title", termo_titulo, dados_filtrados)
        if autor:
            dados_filtrados = filtrar("authors", autor, dados_filtrados)
        if palavra_chave:
            dados_filtrados = filtrar("key_words", palavra_chave, dados_filtrados)
        
        return dados_filtrados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dados: {str(e)}")

@app.get("/anais2024/apresentacoes", response_model=List[TrabalhoAcademico], tags=["Trabalhos Acadêmicos"])
def get_apresentacoes(
    termo_titulo: Optional[str] = Query(None, description="Termo para busca no título das apresentações"),
    autor: Optional[str] = Query(None, description="Nome do autor para busca nas apresentações"),
    palavra_chave: Optional[str] = Query(None, description="Palavra-chave para busca nas apresentações")
):
    """
    Retorna apenas os trabalhos do tipo Apresentação Oral
    
    Permite filtrar as apresentações por:
    - **termo_titulo**: Busca por termo no título da apresentação
    - **autor**: Busca por nome do autor
    - **palavra_chave**: Busca por palavra-chave
    
    Se nenhum filtro for aplicado, retorna todas as apresentações orais.
    """
    try:
        dados = carregar_dados_json(DATA_JSON)
        apresentacoes = list(filter(lambda trabalho: trabalho["work_type"] == "Apresentação Oral", dados))
        
        def filtrar(campo, valor, lista):
            return list(filter(lambda trabalho: valor.lower() in str(trabalho[campo]).lower(), lista))
        
        dados_filtrados = apresentacoes
        
        if termo_titulo:
            dados_filtrados = filtrar("title", termo_titulo, dados_filtrados)
        if autor:
            dados_filtrados = filtrar("authors", autor, dados_filtrados)
        if palavra_chave:
            dados_filtrados = filtrar("key_words", palavra_chave, dados_filtrados)
        
        return dados_filtrados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dados: {str(e)}")


@app.get("/anais2024/exposicoes", response_model=List[TrabalhoAcademico], tags=["Trabalhos Acadêmicos"])
def get_exposicoes(
    termo_titulo: Optional[str] = Query(None, description="Termo para busca no título das exposições"),
    autor: Optional[str] = Query(None, description="Nome do autor para busca nas exposições"),
    palavra_chave: Optional[str] = Query(None, description="Palavra-chave para busca nas exposições")
):
    """
    Retorna apenas os trabalhos do tipo Exposição
    
    Permite filtrar as exposições por:
    - **termo_titulo**: Busca por termo no título da exposição
    - **autor**: Busca por nome do autor
    - **palavra_chave**: Busca por palavra-chave
    
    Se nenhum filtro for aplicado, retorna todas as exposições.
    """
    try:
        dados = carregar_dados_json(DATA_JSON)
        exposicoes = list(filter(lambda trabalho: trabalho["work_type"] == "Exposição", dados))
        
        def filtrar(campo, valor, lista):
            return list(filter(lambda trabalho: valor.lower() in str(trabalho[campo]).lower(), lista))
        
        dados_filtrados = exposicoes
        
        if termo_titulo:
            dados_filtrados = filtrar("title", termo_titulo, dados_filtrados)
        if autor:
            dados_filtrados = filtrar("authors", autor, dados_filtrados)
        if palavra_chave:
            dados_filtrados = filtrar("key_words", palavra_chave, dados_filtrados)
        
        return dados_filtrados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dados: {str(e)}")


@app.get("/anais2024/estatisticas", response_model=EstatisticasGerais, tags=["Estatísticas"])
def get_estatisticas():
    """
    Retorna estatísticas gerais dos trabalhos acadêmicos
    
    Fornece informações como:
    - Total de trabalhos
    - Total de apresentações orais
    - Total de exposições  
    - Número de autores únicos
    """
    try:
        dados = carregar_dados_json(DATA_JSON)
        
        total_trabalhos = len(dados)
        total_apresentacoes = len([t for t in dados if t["work_type"] == "Apresentação Oral"])
        total_exposicoes = len([t for t in dados if t["work_type"] == "Exposição"])
        
        return {
            "total_trabalhos": total_trabalhos,
            "total_apresentacoes": total_apresentacoes,
            "total_exposicoes": total_exposicoes,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dados: {str(e)}")


# Endpoints para busca de resultado único usando {} (path parameters)

@app.get("/anais2024/pagina/{page_number}", response_model=TrabalhoAcademico, tags=["Busca Única"])
def get_trabalho_por_pagina(page_number: int):
    """
    Retorna o trabalho específico de uma página
    
    **page_number**: Número da página do trabalho no documento
    
    Retorna um único trabalho localizado na página especificada.
    """
    try:
        dados = carregar_dados_json(DATA_JSON)
        trabalho = next((t for t in dados if t["page_number"] == page_number), None)
        
        if not trabalho:
            raise HTTPException(status_code=404, detail=f"Trabalho na página {page_number} não encontrado")
        
        return trabalho
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dados: {str(e)}")


@app.get("/anais2024/titulo/{titulo}", response_model=TrabalhoAcademico, tags=["Busca Única"])
def get_trabalho_por_titulo_exato(titulo: str):
    """
    Retorna o trabalho com título exato especificado
    
    **titulo**: Título completo e exato do trabalho (case-insensitive)
    
    Retorna um único trabalho que corresponde exatamente ao título fornecido.
    """
    try:
        dados = carregar_dados_json(DATA_JSON)
        trabalho = next((t for t in dados if t["title"].lower() == titulo.lower()), None)
        
        if not trabalho:
            raise HTTPException(status_code=404, detail=f"Trabalho com título '{titulo}' não encontrado")
        
        return trabalho
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dados: {str(e)}")


