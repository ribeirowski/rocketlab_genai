# 🚀 Agente de Text-to-SQL para E-Commerce

Um assistente de dados inteligente que traduz perguntas em linguagem natural em consultas SQL precisas para analisar dados de e-commerce. Construído com **FastAPI** e alimentado pelo **Google Gemini**.

---

## ✨ Funcionalidades

- **Interface em Linguagem Natural**: Interaja com seu banco de dados usando linguagem simples.
- **Geração Automática de SQL**: Utiliza o Google Gemini para gerar consultas SQLite3 otimizadas.
- **Análise Inteligente de Dados**: Resume automaticamente os resultados e destaca insights de negócios fundamentais.
- **Segurança e Proteção**: Proteção integrada contra operações SQL destrutivas (drops, deletes, etc.).
- **API Moderna**: Backend assíncrono com endpoints autodocumentados (Swagger/OpenAPI).
- **Segurança de Tipos**: Integração total com Pydantic para validação robusta de requisições e respostas.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: [Python 3.13+](https://www.python.org/)
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **LLM**: [Google Gemini Pro](https://ai.google.dev/)
- **Banco de Dados**: [SQLite3](https://www.sqlite.org/)
- **Ambiente**: Pydantic Settings & `.env`
- **Gerenciador de Pacotes**: [uv](https://github.com/astral-sh/uv)

## 🚦 Introdução

### Pré-requisitos

- Python 3.13+ instalado.
- Uma chave de API do Google AI Studio. [Obtenha uma aqui](https://aistudio.google.com/).
- [uv](https://github.com/astral-sh/uv) instalado (recomendado).

### Instalação e Configuração

1. **Clone o repositório**:

   ```bash
   git clone <url-do-repositorio>
   cd rocketlab_genai/server
   ```
2. **Instale as dependências**:

   ```bash
   uv sync
   ```
3. **Configure as Variáveis de Ambiente**:
   Crie um arquivo `.env` no diretório `server`:

   ```env
   GEMINI_API_KEY="sua_chave_api_aqui"
   ```

### Executando a Aplicação

Inicie o servidor de desenvolvimento com:

```bash
uv run uvicorn app.main:app --reload
```

O servidor estará rodando em `http://localhost:8000`.

## 📖 Uso da API

### Check de Saúde (Health Check)

Verifique se a API e a conexão com o banco de dados estão funcionando corretamente.

- **URL**: `/api/v1/health`
- **Método**: `GET`

### Query Agent

Faça uma pergunta sobre os dados de e-commerce.

- **URL**: `/api/v1/agent/query`
- **Método**: `POST`
- **Payload**:
  ```json
  {
    "question": "Quais são os 5 produtos mais caros?"
  }
  ```

## 📂 Estrutura do Projeto

```text
server/
├── app/
│   ├── main.py          # Ponto de entrada da aplicação e config do FastAPI
│   ├── config.py        # Gerenciamento de configurações via Pydantic
│   ├── dependencies.py  # Configuração de injeção de dependência
│   ├── exceptions.py    # Classes de exceção personalizadas
│   ├── routers/         # Definições de rotas da API
│   ├── services/        # Lógica de negócio e integração com LLM
│   ├── repositories/    # Camada de acesso ao banco de dados
│   └── schemas/         # Modelos Pydantic para dados da API
├── banco.db             # Arquivo do banco de dados SQLite
├── pyproject.toml       # Dependências e metadados do projeto
└── .env                 # Segredos de ambiente (não versionado)
```

---

Gerado com ❤️ por Antigravity.
