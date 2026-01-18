from typing import Literal, Optional

from pydantic import BaseModel, Field


class AnalyzisTextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Texto do email para classificar",
    )


class AnalyzisResponse(BaseModel):
    category: Literal["Produtivo", "Improdutivo"]
    confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=1,
        description="Confianca opcional entre 0 e 1",
    )
    reply: Optional[str] = Field(
        default=None,
        description="Resposta sugerida ao email",
    )
    needs_review: bool = Field(
        default=False,
        description="Marca casos ambiguos para revisao manual",
    )
    extracted_text: Optional[str] = Field(
        default=None,
        description="Texto extraído do documento (últimos 500 caracteres se maior)",
    )


class AnalyzisErrorResponse(BaseModel):
    detail: str


class FeedbackResponse(BaseModel):
    success: bool = Field(
        default=True,
        description="Indica se o feedback foi salvo com sucesso"
    )
    message: str = Field(
        default="Feedback registrado com sucesso",
        description="Mensagem de retorno"
    )