import datetime
from time import timezone
from fastapi import FastAPI


app = FastAPI(
    title="MAIl Check API",
    description="Backend MAIl Check para classificação de emails",
    version="1.0.0"
)


@app.get("/health")
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