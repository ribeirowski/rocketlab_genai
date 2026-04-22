# RocketLab Frontend

Front-end React + Vite para integrar com o backend em `server/`.

Como executar:

1. Entre na pasta `web`:

```pwsh
cd web
```

2. Instale dependências:

```pwsh
npm install
```

3. Rode em modo dev:

```pwsh
npm run dev
```

O frontend espera o backend disponível em `http://localhost:8000/api/v1` por padrão. Para apontar para outro host, crie um arquivo `.env` com:

```
VITE_API_BASE=http://localhost:8000/api/v1
```

Observações:
- Componentes minimalistas estilo shadcn foram implementados com Tailwind (local). Você pode trocar por uma instalação oficial do shadcn UI depois.

Novidades nesta versão:
- UI em estilo branco/preto, com layout em cartão e bolhas de mensagem.
- Animação de carregamento (skeleton shimmer) exibida enquanto a API responde.
- Resposta do assistente formatada: análise (parágrafos), SQL em bloco monoespaçado e tabela de dados.

Onde editar:
- Componentes: `src/components/` (Chat, AssistantMessage, ChatMessage, LoadingSkeleton)
- Estilos: `src/index.css`
