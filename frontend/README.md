# M-AI-l Check Frontend

Frontend para o classificador de emails com inteligência artificial.

## Stack

- **Next.js 16** (App Router)
- **React 19**
- **Tailwind CSS 4**
- **TypeScript**

## Estrutura

```
frontend/src/
├── app/
│   ├── layout.tsx          # Layout base
│   ├── page.tsx            # Pagina principal
│   ├── globals.css         # Estilos Tailwind
│   └── api/
│       └── analyze/
│           └── route.ts    # Proxy para backend
├── components/
│   ├── EmailForm.tsx       # Formulario de upload/texto
│   └── ResultCard.tsx      # Card de resultado
└── types.ts                # Tipos TypeScript
```

## Instalacao

```bash
cd frontend
npm install
```

## Configuracao

Crie um arquivo `.env.local`:

```env
BACKEND_URL=http://localhost:8000
```

## Execucao

```bash
# Desenvolvimento
npm run dev

# Build
npm run build

# Producao
npm start
```

## Funcionalidades

- Upload de arquivos .txt e .pdf (max 5MB)
- Entrada de texto direto
- Classificacao: Produtivo ou Improdutivo
- Resposta sugerida com botao de copiar
- Indicador de confianca
- Aviso de revisao manual

## Endpoints

| Rota | Metodo | Descricao |
|------|--------|-----------|
| `/api/analyze` | POST | Proxy para o backend (file ou text) |

## Deploy

### Vercel

```bash
npm install -g vercel
vercel
```

Configure a variavel `BACKEND_URL` no dashboard da Vercel.
