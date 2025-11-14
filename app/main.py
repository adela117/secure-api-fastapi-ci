import os
import time
import uuid
import logging
from typing import Any, Dict, List

from fastapi import FastAPI, Request, Header, HTTPException, Depends
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# prometheus metrics
from prometheus_fastapi_instrumentator import Instrumentator

# ----- logging -----
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
log = logging.getLogger("secure-api")

# ----- app -----
app = FastAPI(title="Secure API", version=os.getenv("APP_VERSION", "0.1.0"))

# permissive CORS for demo; tighten in real deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ----- security headers -----
@app.middleware("http")
async def set_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
    return response

# ----- structured access log + request id -----
@app.middleware("http")
async def access_log(request: Request, call_next):
    rid = request.headers.get("x-request-id", str(uuid.uuid4()))
    start = time.time()
    response = await call_next(request)
    ms = int((time.time() - start) * 1000)
    response.headers["x-request-id"] = rid
    log.info(
        "rid=%s method=%s path=%s status=%s dur_ms=%d",
        rid, request.method, request.url.path, response.status_code, ms,
    )
    return response

# ----- rate limiting -----
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc):
    return JSONResponse(status_code=429, content={"detail": "Too many requests"})

# ----- simple header API key auth -----
API_KEY = os.getenv("API_KEY", "")

def require_key(x_api_key: str = Header(default="")):
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="invalid or missing API key")

# ----- metrics (/metrics) -----
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

# ----- models -----
class EchoBody(BaseModel):
    message: str
    count: int = 1

class SumBody(BaseModel):
    numbers: List[int]

# ----- endpoints -----
@app.get("/health", tags=["meta"])
@limiter.limit("20/minute")
def health(request: Request) -> Dict[str, Any]:   # <- add request
    return {"status": "ok", "ts": int(time.time())}

@app.post("/echo", tags=["demo"], dependencies=[Depends(require_key)])
def echo(body: EchoBody) -> Dict[str, Any]:
    return {"echo": body.message, "count": body.count, "received_at": int(time.time())}

@app.post("/sum", tags=["demo"], dependencies=[Depends(require_key)])
def sum_numbers(body: SumBody) -> Dict[str, Any]:
    return {"sum": sum(body.numbers)}

@app.get("/version", tags=["meta"])
def version() -> Dict[str, Any]:
    return {
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "commit": os.getenv("GIT_COMMIT_SHA", "dev"),
    }
