from fastapi import FastAPI, HTTPException, Request, Depends, Header, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse, RedirectResponse, HTMLResponse

from app.depends import get_db_session
from app.routes.api_router import api
from app.routes.user_router import user
from app.routes.admin_router import admin


app = FastAPI(
    title="Cadastro de Prestadores de Serviços",
    version="0.0.1",
    description="Protótipo de uma API para gerir um cadastro de prestadores de serviços freelancers. ",
)

app = FastAPI()


app.mount("/static", StaticFiles(directory="static", html="True"), name="static")

app.include_router(user)
app.include_router(api)
app.include_router(admin)


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    return HTMLResponse(
        status_code=exc.status_code,
        content=f"Error {exc.status_code}: {exc.detail}",
    )


@app.get("/")
def get_root():
    return RedirectResponse("/static/index.html")


@app.get("/info", response_class=PlainTextResponse)
def get_info():
    return f"{app.title}, versão {app.version}\nDescrição: {app.description}"


@app.get("/aberto", response_class=PlainTextResponse)
def rota_aberta():
    return "Este endpoint é aberto para acesso público"
