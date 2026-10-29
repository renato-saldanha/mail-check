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

- Tamanho máximo: **4 MB** (limite de corpo de requisição das funções da Vercel é ~4,5 MB)
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
- `MAX_TOKENS` (opcional, padrão 1024)
- `MAX_TEXT_CHARS` (opcional, padrão 50000), `MAX_PDF_PAGES` (opcional, padrão 20)
- `RATE_LIMIT_PER_IP` (padrão 10), `RATE_LIMIT_GLOBAL` (padrão 100) e `RATE_LIMIT_WINDOW_SECONDS` (padrão 3600)

## Demo na Vercel

Backend e frontend são dois projetos Vercel separados (plano gratuito):

| Projeto | Pasta | Variável | Descrição |
|---------|-------|----------|-----------|
| `mail-check-api` | `backend/` | `GOOGLE_API_KEY` | Chave da API do Gemini (cadastre em Production e Preview) |
| `mail-check` | `frontend/` | `BACKEND_URL` | URL de produção do backend, sem barra final (ex: `https://mail-check-api-one.vercel.app`) |

Backend (FastAPI como função Python, Python 3.12 definido em `backend/.python-version`; o entrypoint é `backend/main.py`):
```bash
vercel link --yes --project mail-check-api --cwd backend
vercel env add GOOGLE_API_KEY production --cwd backend
vercel deploy --prod --yes --cwd backend
```
O projeto `mail-check` tem `frontend` como Root Directory, então o deploy dele é feito a partir da raiz do repositório (`vercel deploy --prod --yes`).

Proteções da demo pública:
- Limite de uso por IP e global (padrão: 10 análises por IP e 100 no total por hora). O contador fica em memória; em serverless cada instância tem o seu e ele zera quando a instância é reciclada, então o limite é aproximado. O frontend repassa o IP do visitante no cabeçalho `x-client-ip`.
- Arquivo de até 4 MB, texto de até 50.000 caracteres, PDF de até 20 páginas e `MAX_TOKENS` limitando a saída.
- Sem `GOOGLE_API_KEY` o `GET /api/health` funciona e as análises retornam 503 com mensagem clara; cota do Gemini esgotada retorna 429.
- Sem disco persistente: o feedback é registrado nos logs da função (`/tmp` não persiste entre invocações).

Limites do plano gratuito do Gemini: a chave gratuita tem limites de requisições por minuto e por dia e de tokens por minuto, que mudam com o tempo e com o modelo (consulte https://ai.google.dev/gemini-api/docs/rate-limits). Ao estourar, a demo exibe "A cota gratuita do Gemini foi atingida" e volta a funcionar quando a cota renova. No plano gratuito o Gemini pode usar os dados enviados para melhorar produtos do Google, por isso use apenas dados fictícios.

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

## Links públicos
- **Aplicação (Vercel):** https://mail-check-chi.vercel.app/
- **Backend (Vercel):** https://mail-check-api-one.vercel.app
- **Vídeo demonstrativo:** https://www.youtube.com/watch?v=OWxhQPaOtCo

## Ajuste de IA (estratégia simples)
- **Few-shot no prompt:** incluir 2–3 exemplos curtos (Produtivo/Improdutivo) para reduzir ambiguidade.
- **Avaliação com feedbacks:** usar o `feedback.json` para amostrar casos corrigidos, medir acurácia e ajustar o prompt.
- **Critério de revisão:** marcar `needs_review` quando houver baixa confiança ou conflito semântico.

## Documentação de ajuste/treinamento (processo aplicado)
Esta solução utiliza **ajuste por prompt (few-shot) + ciclo de feedback** para melhorar a qualidade sem treinar um modelo próprio.

### 1) Few-shot (ajuste de prompt)
Inclua exemplos rotulados no prompt para reduzir ambiguidades entre Produtivo e Improdutivo. Exemplo de bloco:
```
Exemplos:
Email: "Bom dia, preciso atualizar meu chamado #123."
Categoria: Produtivo
Resposta: "Olá! Vamos atualizar seu chamado e retornaremos em breve."

Email: "Feliz Natal para toda a equipe!"
Categoria: Improdutivo
Resposta: "Obrigado pela mensagem! Desejamos um excelente fim de ano."
```

### 2) Avaliação com feedbacks
O endpoint de feedback salva correções em `backend/feedback.json`. Periodicamente:
1. Exporte os registros corrigidos.
2. Calcule acurácia simples: `corretos / total`.
3. Revise os erros mais comuns e ajuste o prompt (ex.: regras de prioridade).

### 3) Critério de revisão manual
Marque `needs_review=true` quando:
- Confiança < 0.6; ou
- O texto contiver sinais conflitantes (elogio + solicitação).

## Próximos passos
- Refinar prompts e validação do JSON do Gemini.