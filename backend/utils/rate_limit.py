import threading
import time
from collections import deque

from fastapi import HTTPException, Request

from utils.utils import get_int_env

# Contadores em memória: em serverless cada instância tem o seu, então o limite é aproximado
_lock = threading.Lock()
_hits_by_ip: dict[str, deque] = {}
_global_hits: deque = deque()


# Descobre o IP do visitante (o proxy do frontend repassa em x-client-ip)
def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-client-ip") or request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "desconhecido"


# Remove timestamps fora da janela
def _prune(hits: deque, limit_time: float) -> None:
    while hits and hits[0] <= limit_time:
        hits.popleft()


# Dependência que limita o uso por IP e o uso global dentro de uma janela de tempo
def rate_limit(request: Request) -> None:
    """
    Limita requisições por IP e no total.

    Variáveis: RATE_LIMIT_PER_IP (10), RATE_LIMIT_GLOBAL (100), RATE_LIMIT_WINDOW_SECONDS (3600)

    Raises:
        HTTPException: 429 quando algum limite é excedido
    """
    per_ip = get_int_env("RATE_LIMIT_PER_IP", 10)
    global_limit = get_int_env("RATE_LIMIT_GLOBAL", 100)
    window = get_int_env("RATE_LIMIT_WINDOW_SECONDS", 3600)

    now = time.time()
    limit_time = now - window
    ip = get_client_ip(request)

    with _lock:
        # Evita crescimento indefinido do dicionário
        if len(_hits_by_ip) > 1000:
            for key in list(_hits_by_ip):
                _prune(_hits_by_ip[key], limit_time)
                if not _hits_by_ip[key]:
                    del _hits_by_ip[key]

        ip_hits = _hits_by_ip.setdefault(ip, deque())
        _prune(ip_hits, limit_time)
        _prune(_global_hits, limit_time)

        if len(ip_hits) >= per_ip:
            retry_after = int(ip_hits[0] + window - now) + 1
            raise HTTPException(
                status_code=429,
                detail=f"Limite de uso da demo atingido ({per_ip} análises por {window // 60} minutos). Tente novamente mais tarde.",
                headers={"Retry-After": str(retry_after)},
            )
        if len(_global_hits) >= global_limit:
            retry_after = int(_global_hits[0] + window - now) + 1
            raise HTTPException(
                status_code=429,
                detail="A demo recebeu muitas análises no momento. Tente novamente mais tarde.",
                headers={"Retry-After": str(retry_after)},
            )

        ip_hits.append(now)
        _global_hits.append(now)
