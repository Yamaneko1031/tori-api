# main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api import user, word, system, tag

app = FastAPI()

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

app.include_router(system.router)
app.include_router(tag.router)
app.include_router(user.router)
app.include_router(word.router)