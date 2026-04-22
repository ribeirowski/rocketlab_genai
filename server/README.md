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
- **Frontend integrado**: Uma interface React + Vite (na pasta `web/`) foi adicionada para facilitar perguntas e visualização dos resultados.
- **Melhorias de robustez**: o serviço agora evita que o LLM consulte tabelas internas de auditoria (questions, query_history, feedback) e tenta uma regeneração guiada quando o SQL gerado referencia tabelas que não existem.
- **Scripts utilitários**: adicionados `server/scripts/inspect_db.py` (inspeção rápida do banco) e `server/scripts/seed_sample_business.py` (cria tabelas de exemplo produtos/itens_venda para testes).

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

   ### Novidades e utilitários adicionados

   - `server/scripts/inspect_db.py`: lista tabelas existentes, contagens e amostras — útil para debug rápido do banco.
   - `server/scripts/seed_sample_business.py`: cria tabelas `produtos` e `itens_venda` com dados de exemplo (somente para ambiente de desenvolvimento/testes).
   - Frontend: pasta `web/` contém um app React + Vite com UI de chat. O dev server do Vite está configurado para proxiar `/api` para `http://localhost:8000` durante o desenvolvimento.

   Para usar os utilitários (exemplos):

   ```pwsh
   python server/scripts/inspect_db.py
   python server/scripts/seed_sample_business.py
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
web/                    # Frontend React + Vite (chat UI)
```

---

Gerado com ❤️ por Antigravity.
