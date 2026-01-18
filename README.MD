# M-AI-l Check — Classificador de Emails com Gemini

Projeto para classificar emails como **Produtivo** ou **Improdutivo** e sugerir respostas automáticas usando o Gemini. O backend é feito em FastAPI e o frontend é construído com Next.js 16 e React 19.

## Visão geral
- Classificação binária via prompt no Gemini.
- Resposta sugerida baseada na categoria.
- Upload de arquivo `.txt`/`.pdf` ou envio de texto direto.
- Backend pronto para rodar localmente e em ambiente serverless.

## Arquitetura (alto nível)
```
Frontend (Next.js) -> API Route (proxy) -> FastAPI (/api) -> Gemini
                                              |-> Classificação
                                              |-> Resposta sugerida
```

## Estrutura de pastas
- `backend/`: API FastAPI, modelos e integração Gemini.
- `frontend/`: UI Next.js (React 19 + Tailwind CSS 4).
- `PLAN.md`: roteiro de desenvolvimento.
- `REQUISITOS.MD`: descrição do desafio.

## Requisitos
- Python **3.12**
- Pip
- Node.js **18+**
- npm

## Configuração rápida (backend)
1. Instale dependências:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Defina a chave do Gemini:
   ```powershell
   $env:GOOGLE_API_KEY="SUA_CHAVE_AQUI"
   ```
3. (Opcional) Ajuste limites:
   - `MAX_TOKENS` (número máximo de tokens de saída do modelo)

## Execução local
Os imports são relativos ao `backend`, então rode a API dentro dessa pasta:
```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Endpoint de saúde:
```
GET http://127.0.0.1:8000/api/health
```

### Frontend
Em outro terminal, rode o frontend:
```bash
cd frontend
npm install
npm run dev
```

Acesse em: http://localhost:3000

## Endpoints

### `GET /api/health`
Retorna status da API.

**Exemplo de resposta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

### `POST /api/analyze/file`
Analisa arquivo `.txt` ou `.pdf`.

- Tamanho máximo: **5 MB**
- Formatos suportados: **txt**, **pdf**

**Exemplo (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/analyze/file" `
  -Method Post `
  -Form @{ file = Get-Item "C:\caminho\email.txt" }
```

### `POST /api/analyze/text`
Analisa texto enviado diretamente por form.

**Exemplo (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/analyze/text" `
  -Method Post `
  -Form @{ text = "Olá, gostaria de atualizar meu chamado..." }
```

**Resposta esperada (para ambos os endpoints):**
```json
{
  "category": "Produtivo",
  "confidence": 0.85,
  "reply": "Resposta sugerida...",
  "needs_review": false
}
```

## Comportamento atual
- PDF é lido com `PyPDF2`.
- TXT tenta múltiplos encodings (`utf-8`, `latin-1`, `cp1252`).
- Se o modelo não retornar JSON válido, há fallback simples para preencher os campos.

## Variáveis de ambiente
- `GOOGLE_API_KEY` (obrigatória)
- `MAX_TOKENS` (opcional)

## Notas de segurança
- PII (emails, telefones, CPF, CNPJ) é automaticamente sanitizado antes de enviar ao Gemini.
- O tamanho de arquivos é limitado para reduzir custos e timeouts.

## Deploy na Nuvem

### Backend (Railway)
1. Crie uma conta no [Railway](https://railway.app)
2. Conecte seu repositório GitHub
3. Selecione a pasta `backend/` como root
4. Configure as variáveis de ambiente:
   - `GOOGLE_API_KEY`: sua chave da API do Gemini
5. O Railway detectará automaticamente o `Procfile` ou `railway.toml`

### Frontend (Vercel)
1. Crie uma conta na [Vercel](https://vercel.com)
2. Importe seu repositório GitHub
3. Selecione a pasta `frontend/` como root
4. Configure as variáveis de ambiente:
   - `BACKEND_URL`: URL do backend no Railway (ex: `https://seu-app.railway.app`)
5. Clique em Deploy

### Variáveis de ambiente por plataforma

| Plataforma | Variável | Descrição |
|------------|----------|-----------|
| Railway | `GOOGLE_API_KEY` | Chave da API do Gemini |
| Vercel | `BACKEND_URL` | URL do backend (Railway) |

## Próximos passos
- Refinar prompts e validação do JSON do Gemini.