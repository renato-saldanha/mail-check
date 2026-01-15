# Plano de Desenvolvimento — Classificador de Emails com Gemini

## Visão Geral
- App web simples para classificar emails em Produtivo/Improdutivo e sugerir respostas automáticas.
- Backend Python (FastAPI) integrando Gemini para classificação e resposta.
- Frontend HTML/CSS/JS para upload de .txt/.pdf ou texto colado.
- Deploy serverless sugerido: Vercel, Render ou Railway.

## Arquitetura (alto nível)
```mermaid
flowchart TD
  user[Usuario] --> ui[Frontend HTML]
  ui --> api[FastAPI /api]
  api --> nlp[Pre-processamento]
  nlp --> gemini[Gemini API]
  gemini --> clf[Classificacao Prod/Improd]
  gemini --> resp[Resposta sugerida]
  clf --> ui
  resp --> ui
```

## Etapas por Fase
1) Planejamento
   - Escolher alvo de deploy (Vercel/Render/Railway).
   - Definir formato de variaveis de ambiente (chave Gemini, limites de tamanho).
2) Backend (FastAPI)
   - Criar endpoints `/api/health` e `/api/analyze`.
   - Implementar leitura de texto (.txt direto; .pdf com extracao).
   - Pre-processar (lowercase, stopwords, normalizacao basica; opcional lematizacao).
   - Montar prompt de classificacao (Produtivo/Improdutivo) com exemplos.
   - Montar prompt de resposta condicionado a categoria; fallback seguro se ambigua.
   - Adicionar limites de tamanho e sanitizacao basica (remover PII simples quando possivel).
3) Frontend
   - Form upload (.txt/.pdf) e textarea de texto colado.
   - Botao de enviar para processamento; estado de carregamento.
   - Exibir categoria, confianca (se fornecida), resposta sugerida; botao de copiar.
   - Mensagens de erro claras (tipo de arquivo, tamanho, falha de API).
4) Observabilidade e Qualidade
   - Logs basicos sem PII; marcar casos ambigos como “revisar”.
   - Botao opcional “corrigir classificacao” para feedback manual (persistencia simples ou mock).
5) Deploy
   - Ajustar configuracao do alvo escolhido (env vars, timeout, build).
   - Gerar instrucoes no README para execucao local e deploy.
   - Opcional: Dockerfile para portabilidade.

## Entregaveis Esperados
- Este `PLAN.md` na raiz.
- `backend/` com FastAPI + integracao Gemini.
- `frontend/` (ou `public/`) com HTML/CSS/JS da interface.
- `requirements.txt` ou `pyproject.toml`; `README.md` com setup e deploy.
- Opcional: Dockerfile.

## Tarefas (checklist)
- [ ] Confirmar alvo de deploy.
- [ ] Implementar FastAPI com integracao Gemini.
- [ ] Criar UI de upload/texto e integracao com API.
- [ ] Testar prompts e ajustar classificacao/resposta.
- [ ] Documentar e preparar deploy na nuvem.



