import logging
import os

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("gateway")

app = FastAPI(title="API Gateway", docs_url=None, redoc_url=None, openapi_url=None)

SERVICES = {
    "products": os.getenv("PRODUCTS_URL", "http://localhost:8001"),
    "users": os.getenv("USERS_URL", "http://localhost:8002"),
    "orders": os.getenv("ORDERS_URL", "http://localhost:8003"),
    "payments": os.getenv("PAYMENTS_URL", "http://localhost:8004"),
}

_HOP_BY_HOP = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
               "te", "trailers", "transfer-encoding", "upgrade", "content-length", "host"}


def _clean_headers(headers: dict) -> dict:
    return {k: v for k, v in headers.items() if k.lower() not in _HOP_BY_HOP}


@app.get("/health")
async def health():
    results = {}
    async with httpx.AsyncClient(timeout=2.0) as client:
        for name, url in SERVICES.items():
            try:
                resp = await client.get(f"{url}/health")
                results[name] = {"ok": resp.status_code == 200}
            except Exception:
                results[name] = {"ok": False}
    return {"status": "ok", "services": results}


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(path: str, request: Request):
    service = path.split("/", 1)[0]
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    url = f"{SERVICES[service]}/{path}"
    headers = _clean_headers(dict(request.headers))
    body = await request.body()

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.request(
            request.method,
            url,
            headers=headers,
            content=body,
            params=dict(request.query_params),
        )

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=_clean_headers(dict(resp.headers)),
    )
