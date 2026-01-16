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


class AnalyzisErrorResponse(BaseModel):
    detail: str