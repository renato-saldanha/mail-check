from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., description="Status da API")
    timestamp: str = Field(..., description="Timestamp ISO-8601 em UTC")
    version: str = Field(..., description="Versao da API")
