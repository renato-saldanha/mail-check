from typing import Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
import logging
import json
import re
import io
import os
from datetime import datetime, timezone

from models.analyze import AnalyzisResponse, FeedbackResponse
from utils.utils import get_llm, sanitize_pii

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["analyze"])


# Função para extrair texto de arquivo TXT
def extract_text_from_txt(file_content: bytes) -> str:
    """
    Extrai texto de um arquivo TXT

    Args:
        file_content: Conteúdo do arquivo em bytes

    Returns:
        str: Texto extraído do arquivo

    Raises:
        HTTPException: Se houver erro ao ler o arquivo
    """
    try:
        # Tenta diferentes encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                return file_content.decode(encoding)
            except UnicodeDecodeError:
                continue
        # Se nenhum encoding funcionar, usa utf-8 com tratamento de erros
        return file_content.decode('utf-8', errors='ignore')
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao ler arquivo TXT: {str(e)}"
        )


# Função para extrair texto de arquivo PDF
def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extrai texto de um arquivo PDF

    Args:
        file_content: Conteúdo do arquivo em bytes

    Returns:
        str: Texto extraído do PDF

    Raises:
        HTTPException: Se houver erro ao processar o PDF ou se a biblioteca não estiver instalada
    """
    try:
        import PyPDF2
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""

        # Extrai texto de todas as páginas
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"

        # Valida se conseguiu extrair texto
        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Não foi possível extrair texto do PDF. O arquivo pode estar protegido ou ser uma imagem."
            )

        return text.strip()
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="Biblioteca PyPDF2 não instalada. Execute: pip install PyPDF2"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao processar PDF: {str(e)}"
        )


# Método que usa llm para analisar o texto
async def analyze_text_gemini(text: str) -> AnalyzisResponse:
    """
    Analisa o texto usando Gemini e retorna classificação e resposta
    """

    prompt = f"""Analise o texto fornecido e:
1. Aplique uma categorização de: Produtivo ou Improdutivo.
- **Produtivo:** Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).
- **Improdutivo:** Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos).

2. Gere uma resposta adequada à classificação realizada:
- **Produtivo:** uma resposta profissional e útil.
- **Improdutivo:** uma resposta educada e breve ou uma sugestão de descartar.

Texto para analisar:
---
{text}
---

Formato da resposta:
{{
    "category": "Produtivo" ou "Improduvito",
    "confidence": 0.0 a 1.0,
    "reply": "resposta sugerida",
    "needs_review": true ou false,
}}"""

    try:
        # Define a llm
        llm = get_llm()

        # invoca a llm e retorna a resposta
        response = await llm.ainvoke(prompt)

        # Extrai o conteúdo
        response_text = response.content

        # Procura um JSON no conteúdo
        json_match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            # Fallback: tentar extrair informações manualmente
            category = "Produtivo" if "produtivo" in response_text.lower() else "Improdutivo"
            confidence = 0.7
            reply = response_text
            needs_review = True

            result = {
                "category": category,
                "confidence": confidence,
                "reply": reply,
                "needs_review": needs_review,
            }

        return AnalyzisResponse(
            category=result.get("category"),
            confidence=result.get("confidence"),
            reply=result.get("reply"),
            needs_review=result.get("needs_review"),
        )

    except Exception as e:
        logger.error(f"Erro ao analisar texto com Gemini: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao analisar o texto com Gemini:\n {e}"
        )


# Endpoint de análise de documentos
@router.post("/analyze/file", response_model=AnalyzisResponse)
async def analyze_documents(file: UploadFile = File(...)):
    """
    Endpoint de analise de arquivos formato PDF e txt

    Args: file-> UploadFile

    Return: 
        200 - Variável tipo AnalysisResponse
        400 - Arquivo com problema em alguma parte do processo
    """
    logger.info(f"Recebida requisição de análise de arquivo: {file.filename if file.filename else 'sem nome'}")

    # Validação da existência do arquivo
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Nome do arquivo não fornecido."
        )

    # Recupera a extensão do arquivo
    file_extension = file.filename.lower().split(".")[-1]

    # Verifica se a extensão do arquivo está nas suportadas
    if file_extension not in ["txt", "pdf"]:
        raise HTTPException(
            status_code=400,
            detail="Formato do arquivo não suportado."
        )

    # Valida o tamanho do arquivo (5mb)
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Tamanho do arquivo excede o tamanho máximo suportado (5mb)."
        )

    # Extrai o arquivo conforme o formato
    match file_extension:
        case "txt":
            text = extract_text_from_txt(file_content)
        case "pdf":
            text = extract_text_from_pdf(file_content)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail=f"O arquivo esta vázio ou contém texto ilegível.\n {text}"
        )

    # Sanitiza PII antes de enviar ao modelo
    sanitized_text = sanitize_pii(text)

    # Analisa com o modelo
    result = await analyze_text_gemini(sanitized_text)
    result.extracted_text = text[500:] if len(text) > 500 else text

    logger.info(f"Análise concluída - Categoria: {result.category}, Confiança: {result.confidence}")
    return result


# Endpoint de análise de texto direto
@router.post("/analyze/text", response_model=AnalyzisResponse)
async def analyze_text(text: str = Form(...)):
    """
    Analisa texto enviados diretamente 
    """
    logger.info(f"Recebida requisição de análise de texto ({len(text)} caracteres)")

    if not text or not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Texto não foi fornecido",
        )

    # Sanitiza PII antes de enviar ao modelo
    sanitized_text = sanitize_pii(text)

    # Efetua analise com llm
    response = await analyze_text_gemini(sanitized_text)
    response.extracted_text = text[500:] if len(text) > 500 else text

    logger.info(f"Análise concluída - Categoria: {response.category}, Confiança: {response.confidence}")
    return response


# Endpoint original
@router.post("/analyze", response_model=AnalyzisResponse)
async def analyze(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
):
    """
    Analisa documento ou texto.
    Aceita documentos: .txt e .pdf ou texto direto via form.
    """

    if file:
        return await analyze_documents(file)
    elif text:
        return await analyze_text(text)
    else:
        raise HTTPException(
            status_code=400,
            detail="Forneça um arquivo para análise. "
        )


# Caminho do arquivo de feedback
FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "feedback.json")


# Endpoint para receber feedback de correção
@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    original_category: str = Form(...),
    corrected_category: str = Form(...),
    text_preview: str = Form(...)
):
    """
    Recebe feedback do usuário para corrigir a classificação.
    Salva em arquivo JSON para análise posterior.
    """
    logger.info(f"Feedback recebido: {original_category} -> {corrected_category}")

    try:
        # Carrega feedbacks existentes
        feedbacks = []
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
                feedbacks = json.load(f)

        # Adiciona novo feedback
        feedback_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "original_category": original_category,
            "corrected_category": corrected_category,
            "text_preview": text_preview[:100]  # Limita a 100 caracteres
        }
        feedbacks.append(feedback_entry)

        # Salva no arquivo
        with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
            json.dump(feedbacks, f, ensure_ascii=False, indent=2)

        return FeedbackResponse(
            success=True,
            message="Feedback registrado com sucesso"
        )

    except Exception as e:
        logger.error(f"Erro ao salvar feedback: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao salvar feedback: {str(e)}"
        )
