import os
from .download_pdf import download
from .pdf_extract import extrair_dados
from .save_as_json import salvar_dados_como_json
from .load_json import limpar_cache


def inicializar_dados(url, arquivo_pdf, arquivo_json):
    """
    Inicializa os dados fazendo download do PDF, extraindo dados e salvando como JSON.
    Retorna True se tudo ocorreu bem, False caso contrário
    """
    try:
        print(f"Arquivo {arquivo_json} não encontrado. Baixando e extraindo dados...")
        
        status_download = download(url, arquivo_pdf)
        if not status_download:
            print(f"Falha ao baixar o arquivo: {url}")
            return False
            
        dados = extrair_dados(arquivo_pdf)
        if not dados:
            print(f"Falha ao extrair dados do arquivo: {arquivo_pdf}")
            return False
            
        salvar_dados_como_json(dados, arquivo_json)
        # Limpa o cache para garantir que os novos dados sejam carregados
        limpar_cache()
        print(f"Dados inicializados com sucesso em {arquivo_json}")
        return True
        
    except Exception as excecao:
        print(f'Erro ao inicializar dados: {excecao}')
        return False


def garantir_diretorio(caminho):
    """
    Garante que um diretório existe, criando-o se necessário.
    """
    os.makedirs(caminho, exist_ok=True)
