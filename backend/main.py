from fastapi import FastAPI
from datetime import datetime, timezone
from dotenv import load_dotenv
import logging

from models.health import HealthResponse
from routes.v1 import router as analyze_router 

load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="M-AI-l Check API",
    description="Backend M-AI-l Check para classificação de emails",
    version="1.0.0"
)

app.include_router(analyze_router)

# Endpoint de verificação de saúde
@app.get("/api/health", response_model=HealthResponse)
def health_check():
    """
    Endpoint para monitoramento de saúde da API
    """

    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)