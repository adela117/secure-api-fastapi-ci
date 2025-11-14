import os
import time
import logging
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

# basic structured logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
log = logging.getLogger("secure-api")

app = FastAPI(title="Secure API", version=os.getenv("APP_VERSION", "0.1.0"))

# safe default CORS for demo; lock this down in real life
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# security headers (tiny hardening)
@app.middleware("http")
async def set_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
    return response

# request/response timing log
@app.middleware("http")
async def access_log(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    ms = int((time.time() - start) * 1000)
    log.info("%s %s %s %dms", request.method, request.url.path, response.status_code, ms)
    return response

@app.get("/health", tags=["meta"])
def health() -> Dict[str, Any]:
    return {"status": "ok", "ts": int(time.time())}

class EchoBody(BaseModel):
    message: str
    count: int = 1

@app.post("/echo", tags=["demo"])
def echo(body: EchoBody) -> Dict[str, Any]:
    return {"echo": body.message, "count": body.count, "received_at": int(time.time())}

@app.get("/version", tags=["meta"])
def version() -> Dict[str, Any]:
    return {
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "commit": os.getenv("GIT_COMMIT_SHA", "dev"),
    }
