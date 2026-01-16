# M-AI-l Check — Classificador de Emails com Gemini

Projeto para classificar emails como **Produtivo** ou **Improdutivo** e sugerir respostas automáticas usando o Gemini. O backend é feito em FastAPI e a UI será um frontend simples em HTML/CSS/JS.

## Visão geral
- Classificação binária via prompt no Gemini.
- Resposta sugerida baseada na categoria.
- Upload de arquivo `.txt`/`.pdf` ou envio de texto direto.
- Backend pronto para rodar localmente e em ambiente serverless.

## Arquitetura (alto nível)
```
Frontend (HTML/JS) -> FastAPI (/api) -> Pré-processamento -> Gemini
                                           |-> Classificação
                                           |-> Resposta sugerida
```

## Estrutura de pastas
- `backend/`: API FastAPI, modelos e integração Gemini.
- `frontend/`: UI (a construir).
- `PLAN.md`: roteiro de desenvolvimento.
- `REQUISITOS.MD`: descrição do desafio.

## Requisitos
- Python **3.12**
- Pip

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
- Evite enviar PII desnecessária ao modelo.
- O tamanho de arquivos é limitado para reduzir custos e timeouts.

## Próximos passos
- Conectar a UI em `frontend/` aos endpoints da API.
- Refinar prompts e validação do JSON do Gemini.
- Preparar deploy (Railway/Render/Vercel).