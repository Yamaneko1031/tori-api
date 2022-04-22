# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from app.api import user, word, system, tag
from app.webapps import admin


def configure(app):
    #: Configure CORS
    origins = [
        "http://localhost:3000",
        "https://torichan.app",
        "https://tori-front.vercel.app",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.mount("/static", StaticFiles(directory="app/static"), name="static")


def include_router(app):
    app.include_router(system.router)
    app.include_router(tag.router)
    app.include_router(user.router)
    app.include_router(word.router)
    app.include_router(admin.router)


def start_application():
    app = FastAPI()
    configure(app)
    include_router(app)
    return app


app = start_application()

# uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload