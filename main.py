from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from app.logic.core.logging import APILog
from app.router import auth
from app import log
from app.router.router_tags import RouterTags

app = FastAPI()

# Router
app.include_router(auth.router, prefix="/api", tags=[RouterTags.auth])

# Middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=APILog())


@app.get("/")
def read_root():
    try:
        return {"Hello": "Python"}
    except Exception as ex:
        log.critical(ex, exc_info=True)
        raise ex
