from fastapi import FastAPI

from cvm.api.routes import cia_aberta
from cvm.api.internal import admin


# uvicorn cvm.api:api --reload
app = FastAPI(title="CVM")

# includes routes
app.include_router(cia_aberta.routes)
app.include_router(
    admin.routes,
    prefix="/admin",
    tags=["admin"]
)

@app.get('/')
def root():
    return {
        "name": "API REST para os dados abertos da Comissão de Valores Mobiliários",
        "redoc" : "http://localhost:8000/redoc",
        "docs" : "http://localhost:8000/docs",
        "github": "https://www.github.com/dalmofelipe/cvm"
    }
