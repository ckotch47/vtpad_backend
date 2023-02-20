from typing import Union, List

from jose import ExpiredSignatureError, jwt
from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles

from tortoise.contrib.fastapi import register_tortoise

import app.src.common as common
import app.src.items as items

import app.src.pad as pad
import app.src.space as space
import app.src.run as run
import app.src.runitems as runitems
import app.src.users as users
import app.src.auth as auth
import app.src.file as file
import app.src.notes as note

from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.src.common.crypto import user_payload

config = common.EnvConfig()
models = common.Models()

execetion_path = [
    ['POST', '/auth'],
    ['POST', '/user']
]


async def permissions(request: Request):
    path = request.url.path
    if [request.method, path] not in execetion_path:
        token = request.headers.get('authorization')
        await verify_token(token)


async def verify_token(token: str):
    if token is None:
        raise HTTPException(status_code=401, detail="not auth")
    string = token.split(' ')[1]
    try:
        user_payload(string)
    except:
        raise HTTPException(status_code=401, detail="not auth")


app = FastAPI(
    redoc_url='/docs',
    dependencies=[Depends(permissions)]
)

# for cors host
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:8008",
    "*"
]

# settings cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  register orm
register_tortoise(
    app,
    db_url=f'postgres://'
           f'{config.db_user}:{config.db_password}'
           f'@{config.db_host}:{config.db_port}/{config.db_name}',
    modules={"models": models.get_models()},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

app.mount('/uploads', StaticFiles(directory="uploads"), name="uploads")

app.include_router(items.items_router)
app.include_router(pad.pad_router)
app.include_router(space.space_router)
app.include_router(run.runs_router)
app.include_router(runitems.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(file.router)
app.include_router(note.router)
