# 📚 Mostra IFRS Restinga API

API REST para consulta e busca nos dados da **13ª Mostra Científica do IFRS – Campus Restinga**. Esta API extrai automaticamente os dados dos anais em PDF e oferece endpoints para consulta com filtros avançados, busca por dados específicos e estatísticas gerais.

## 🚀 Como rodar o projeto

### Pré-requisitos
- Python 3.8+
- pip

### Instalação

1. **Clone o repositório e acesse a pasta**:
   ```bash
   git clone https://github.com/RaissonGitHub/Mostra-IFRS-Restinga-API.git
   cd Mostra-IFRS-Restinga-API
   ```

2. **(Recomendado) Crie e ative um ambiente virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a API**:
   ```bash
   uvicorn src.main:app --reload
   ```

A API estará disponível em `http://localhost:8000` com documentação automática em `/docs`.

## 📖 Documentação interativa

Após iniciar a API, você pode acessar:

- **Swagger UI**: `http://localhost:8000/docs` - Interface interativa para testar os endpoints
- **ReDoc**: `http://localhost:8000/redoc` - Documentação alternativa mais detalhada

## 📋 Endpoints disponíveis

### Endpoints de listagem
- `GET /` — Mensagem de boas-vindas
- `GET /anais2024` — Lista todos os trabalhos (filtros: termo_titulo, autor, palavra_chave)
- `GET /anais2024/apresentacoes` — Lista apenas apresentações orais
- `GET /anais2024/exposicoes` — Lista apenas exposições

### Endpoints de busca única
- `GET /anais2024/pagina/{page_number}` — Retorna trabalho específico por número da página
- `GET /anais2024/titulo/{titulo}` — Retorna trabalho por título exato

### Endpoints de estatísticas
- `GET /anais2024/estatisticas` — Estatísticas gerais dos trabalhos

### Parâmetros de consulta disponíveis
Todos os endpoints de dados suportam os seguintes filtros (opcionais):

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `termo_titulo` | string | Busca por termo no título do trabalho |
| `autor` | string | Busca por nome do autor |
| `palavra_chave` | string | Busca por palavra-chave |

## 🔍 Exemplos de uso

### Endpoints de listagem com filtros

#### Buscar todos os trabalhos
```http
GET http://localhost:8000/anais2024
```

#### Buscar por título
```http
GET http://localhost:8000/anais2024?termo_titulo=Robótica
```

#### Buscar por autor
```http
GET http://localhost:8000/anais2024?autor=Maria
```

#### Buscar por palavra-chave
```http
GET http://localhost:8000/anais2024?palavra_chave=Educação
```

#### Buscar apenas apresentações orais por título
```http
GET http://localhost:8000/anais2024/apresentacoes?termo_titulo=Inteligência
```

#### Combinar filtros (busca exposições de um autor específico)
```http
GET http://localhost:8000/anais2024/exposicoes?autor=João
```

### Endpoints de busca única

#### Buscar trabalho por página específica
```http
GET http://localhost:8000/anais2024/pagina/15
```

#### Buscar trabalho por título exato
```http
GET http://localhost:8000/anais2024/titulo/Desenvolvimento de Sistema de Monitoramento
```

### Endpoints de estatísticas

#### Obter estatísticas gerais
```http
GET http://localhost:8000/anais2024/estatisticas
```

## 📊 Estrutura dos dados retornados

### Trabalhos acadêmicos
Cada trabalho retornado possui a seguinte estrutura:

```json
{
  "page_number": 15,
  "title": "Desenvolvimento de Sistema de Monitoramento",
  "work_type": "Apresentação Oral",
  "authors": ["João Silva", "Maria Santos"],
  "summary": "Este trabalho apresenta...",
  "key_words": ["Monitoramento", "IoT", "Tecnologia"]
}
```

#### Campos disponíveis:
- **`page_number`**: Número da página no PDF original
- **`title`**: Título completo do trabalho
- **`work_type`**: Tipo do trabalho ("Apresentação Oral" ou "Exposição")
- **`authors`**: Lista com nomes dos autores
- **`summary`**: Resumo completo do trabalho
- **`key_words`**: Lista de palavras-chave

### Estatísticas gerais
O endpoint de estatísticas retorna:

```json
{
  "total_trabalhos": 45,
  "total_apresentacoes": 30,
  "total_exposicoes": 15
}
```

#### Campos das estatísticas:
- **`total_trabalhos`**: Número total de trabalhos nos anais
- **`total_apresentacoes`**: Número total de apresentações orais
- **`total_exposicoes`**: Número total de exposições

## 🛠️ Tecnologias utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno e rápido para APIs
- **[Pydantic](https://pydantic-docs.helpmanual.io/)**: Validação de dados e serialização
- **[PDFPlumber](https://github.com/jsvine/pdfplumber)**: Extração precisa de dados de arquivos PDF
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI de alta performance
- **[Requests](https://docs.python-requests.org/)**: Cliente HTTP para download de arquivos

## 📁 Estrutura do projeto

```
Mostra-IFRS-Restinga-API/
├── src/
│   ├── __init__.py
│   ├── config.py         # Configurações da aplicação
│   ├── download_pdf.py   # Download do PDF dos anais
│   ├── load_json.py      # Carregamento dos dados JSON
│   ├── main.py           # Aplicação FastAPI principal
│   ├── models.py         # Modelo de dados utilizados
│   ├── pdf_extract.py    # Extração de dados do PDF
│   ├── save_as_json.py   # Salvamento dos dados em JSON
│   └── utils.py          # Funções utilitárias
├── data/                 # Diretório de dados (criado automaticamente)
├── requirements.txt      # Dependências do projeto
└── README.md            # Este arquivo
```

## ⚡ Funcionamento interno

1. **Primeira execução**: A API baixa automaticamente o PDF dos anais do repositório oficial do IFRS
2. **Processamento**: Os dados são extraídos do PDF e estruturados em formato JSON
3. **Cache**: Os dados processados são salvos localmente para consultas rápidas
4. **Consultas**: As requisições são atendidas a partir dos dados em cache
