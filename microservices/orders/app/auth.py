import logging
import os
import secrets

from fastapi import Header, HTTPException, status

logger = logging.getLogger("auth")

API_KEY = os.getenv("API_KEY", "dev-api-key")


def require_api_key(x_api_key: str = Header(default="")) -> str:
    if not secrets.compare_digest(x_api_key, API_KEY):
        logger.warning("Falha de autenticação: API key inválida")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida",
        )
    return x_api_key
