import json
import os


# Cache para armazenar os dados carregados
_cache_dados = None
_cache_timestamp = None
_cache_arquivo = None


def carregar_dados_json(arquivo):
    """
    Carrega dados de um arquivo JSON e retorna uma lista de trabalhos.
    Utiliza cache para evitar recarregar o arquivo a cada chamada.
    """
    global _cache_dados, _cache_timestamp, _cache_arquivo
    
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(arquivo):
            return []
            
        # Obtém o timestamp de modificação do arquivo
        timestamp_atual = os.path.getmtime(arquivo)
        
        # Se o cache está vazio ou o arquivo foi modificado, recarrega
        if (_cache_dados is None or 
            _cache_arquivo != arquivo or 
            _cache_timestamp != timestamp_atual):
            
            with open(arquivo, "r", encoding="utf-8") as arq:
                _cache_dados = json.load(arq)
            _cache_timestamp = timestamp_atual
            _cache_arquivo = arquivo
            print(f"Dados carregados do arquivo: {arquivo}")
        
        return _cache_dados
        
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON do arquivo: {arquivo}")
        return []
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return []


def limpar_cache():
    """Limpa o cache de dados JSON."""
    global _cache_dados, _cache_timestamp, _cache_arquivo
    _cache_dados = None
    _cache_timestamp = None
    _cache_arquivo = None
    print("Cache de dados JSON limpo.")