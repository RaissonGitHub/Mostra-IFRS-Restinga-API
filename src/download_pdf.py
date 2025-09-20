import requests
import os


def download(url, nome):
    """Faz o download de um arquivo PDF a partir de uma URL."""
    try:
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(nome), exist_ok=True)
        
        requisicao = requests.get(url)
        requisicao.raise_for_status()
        with open(nome, 'wb') as arquivo:
            arquivo.write(requisicao.content)
        print(f'Sucesso ao baixar o arquivo {nome}')
        return True
    except requests.exceptions.RequestException as erro:
        print(f'Erro no download: {erro}')
        return False
    
