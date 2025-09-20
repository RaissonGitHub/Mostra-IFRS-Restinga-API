from pydantic import BaseModel, Field
from typing import List, Optional


class TrabalhoAcademico(BaseModel):
    """Modelo para representar um trabalho acadêmico da Mostra Científica"""
    page_number: int = Field(..., description="Número da página no documento")
    title: str = Field(..., description="Título do trabalho")
    work_type: str = Field(..., description="Tipo do trabalho (Apresentação Oral ou Exposição)")
    authors: List[str] = Field(..., description="Lista de autores do trabalho")
    summary: str = Field(..., description="Resumo do trabalho")
    key_words: List[str] = Field(..., description="Palavras-chave do trabalho")


class MensagemResposta(BaseModel):
    """Modelo para resposta de mensagem simples"""
    mensagem: str = Field(..., description="Mensagem de resposta da API")


class ListaTrabalhos(BaseModel):
    """Modelo para lista de trabalhos acadêmicos"""
    trabalhos: List[TrabalhoAcademico] = Field(..., description="Lista de trabalhos acadêmicos")
    total: int = Field(..., description="Total de trabalhos encontrados")


class EstatisticasGerais(BaseModel):
    """Modelo para estatísticas gerais dos trabalhos"""
    total_trabalhos: int = Field(..., description="Total de trabalhos")
    total_apresentacoes: int = Field(..., description="Total de apresentações orais")
    total_exposicoes: int = Field(..., description="Total de exposições")
    