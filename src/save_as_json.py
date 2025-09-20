import json
import os


def salvar_dados_como_json(dados, caminho_saida):
    """Salva uma lista de dados como arquivo JSON."""
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    
    with open(caminho_saida, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    print(f"\nSucesso ao converter o arquivo: salvo como '{caminho_saida}'")
