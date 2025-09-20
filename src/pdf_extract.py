import pdfplumber
import re


def extrair_dados(caminho_pdf):
    """Extrai dados dos trabalhos do PDF e retorna uma lista de dicionários."""
    trabalhos_extraidos = []
    # Palavras para ajudar identificar o começo dos resumos
    palavras_inicio_resumo = (
        'O ', 'A ', 'Os ', 'As ', 'Ao', 'Relato', 'Todo', 'Entre', 'Este ', 'Esse', 'Esta ', 'Estes', 'Estas',
        'Sabe-se', 'Considerando', 'Diante', 'Para', 'Segundo', 'Com',
        'Nas ', 'Nos ', 'No ', 'Na ', 'Desde', 'Muito', 'Atualmente',
        'Justamente', 'Dentro', 'Ainda'
    )
    with pdfplumber.open(caminho_pdf) as pdf:
        # Define os primiros trabalhos como apresentação oral
        tipo_trabalho = 'Apresentação Oral'
        # Leitura das páginas e texto delas
        for i in range(6, len(pdf.pages)):
            pagina = pdf.pages[i]
            texto_pagina = pagina.extract_text()

            # Página em branco
            if not texto_pagina:
                continue
            # Retirada de espaços em branco e divisão das linhas
            linhas_texto = [linha.strip() for linha in texto_pagina.strip().split('\n') if linha.strip()]
            
            # Identificar o número da página no final e remove-lo
            if linhas_texto and linhas_texto[-1].isdigit():
                linhas_texto = linhas_texto[:-1]
            
            # Pula linha em branco
            if not linhas_texto:
                continue

            titulo = ""
            indice_fim_titulo = -1
            # Identificação do título do trabalho (Maiúsculo)
            for indice, linha in enumerate(linhas_texto):
                if linha.isupper():
                    titulo += f"{linha} "
                    indice_fim_titulo = indice
                elif titulo:
                    break
            titulo = titulo.strip()
            # Se encontrou a página com a escrita Exposição os trabalhos a seguir são exposições
            if titulo == "EXPOSIÇÃO DE TRABALHOS":
                tipo_trabalho = "Exposição"
                continue

            # Caso o número de palavras-chave ultrapasse mais de uma linha a segunda deve ser considerada
            if ';' in linhas_texto[-2]:
                palavras_chave = linhas_texto[-2:]
                palavras_chave = ' '.join(palavras_chave)
                linhas_meio = linhas_texto[indice_fim_titulo + 1 : -2]
            # Palavras-chave ocupam apenas uma linha
            else:
                palavras_chave = linhas_texto[-1]
                linhas_meio = linhas_texto[indice_fim_titulo + 1 : -1]

            autores = ""
            resumo = ""

            # Identificação do resumo
            indice_inicio_resumo = 0
            for indice, linha in enumerate(linhas_meio):
                if linha.startswith(palavras_inicio_resumo):
                    indice_inicio_resumo = indice
                    break

            # Pega do fim do título até o início do resumo
            autores = " ".join(linhas_meio[:indice_inicio_resumo]).strip()
            # Pega do fim do resumo
            resumo = " ".join(linhas_meio[indice_inicio_resumo:]).strip()

            # Se a formatação for errada, mistura tudo no resumo
            if not resumo:
                autores = ""
                resumo = " ".join(linhas_meio)

            # Retirando informações como (Campus Restinga) e fazendo split da string
            autores_processados = [a.strip() for a in re.sub(r"\(.*?\)", ",", autores).split(',') if a]

            # Corrigindo formatações erradas
            palavras_chave_processadas = palavras_chave.replace('-',';').replace(',',';').replace('.','')
            # Split da sting
            palavras_chave_processadas = [p.strip() for p in palavras_chave_processadas.split(';') if p]
            
            # Estrutura final
            trabalho = {
                "page_number": pagina.page_number,
                "title": titulo,
                "work_type": tipo_trabalho,
                "authors": autores_processados,
                "summary": resumo.replace('―','"').replace('‖', '"'),
                "key_words": palavras_chave_processadas
            }
            # Append
            trabalhos_extraidos.append(trabalho)
    return trabalhos_extraidos

