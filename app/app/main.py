# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from app.api import user, word, system, tag
# from app.webapps import admin


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
    # app.include_router(admin.router)

def start_application():
    app = FastAPI()
    configure(app)
    include_router(app)
    return app

app = start_application()

@app.get("/users")
def read_users():
    return {"id": 1, "name": "taro"}

@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}

# app = FastAPI()

# #: Configure CORS
# origins = [
#     "http://localhost:3000",
#     "https://torichan.app",
#     "https://tori-front.vercel.app",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# app.include_router(system.router)
# app.include_router(tag.router)
# app.include_router(user.router)
# app.include_router(word.router)
# app.include_router(admin.router)

# uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload --proxy-headers --forwarded-allow-ips='*'


# from fastapi import FastAPI
# from starlette.middleware.cors import CORSMiddleware # 追加

# app = FastAPI()

# # CORSを回避するために追加（今回の肝）
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,   # 追記により追加
#     allow_methods=["*"],      # 追記により追加
#     allow_headers=["*"]       # 追記により追加
# )

# @app.get("/users")
# def read_users():
#     return {"id": 1, "name": "taro"}

# @app.get("/users/{user_id}")
# def read_user(user_id: int):
#     return {"user_id": user_id}