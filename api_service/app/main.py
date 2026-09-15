from fastapi import FastAPI

from .routers import ausencias

app = FastAPI(
    title="Ausência RH - API",
    description="API pública para solicitação e aprovação de ausências de colaboradores.",
    version="1.0.0",
)

app.include_router(ausencias.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
