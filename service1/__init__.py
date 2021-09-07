from fastapi import FastAPI, Request
from loguru import logger
from motor import motor_asyncio
from fastapi.middleware.cors import CORSMiddleware
from starlette.routing import Match

import yaml
import secrets
import sys

from .service import UserService

VERSION = "1.0"

config = yaml.safe_load(open("config.yaml", "r"))

logger.add("backend.log", rotation="1 week")
# jwt_secret = secrets.token_hex(32)

try:
    motor = motor_asyncio.AsyncIOMotorClient(config["core"]["mongodb_url"])
    db = motor[config["core"]["mongodb_db"]]
    jwt_algorithm = config["jwt"]["algorithm"]
    jwt_expire = config["jwt"]["expire"]
    username = config["email"]["username"]
    password = config["email"]["password"]
    smtp_server = config["email"]["smtp"]
    port = config["email"]["port"]
    jwt_secret = config["jwt"]["secret"]
except KeyError as e:
    logger.error(f"{e}")
    sys.exit(1)

user_service = UserService(db.users)

app = FastAPI(title="Service 1 Backend", version=VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from .routes import auth, main  # noqa: E402

app.include_router(router=main.router)
app.include_router(router=auth.router)


# https://stackoverflow.com/a/63413392
@app.middleware("http")
async def log_middle(request: Request, call_next):
    logger.debug(f"{request.method} {request.url}")
    routes = request.app.router.routes
    logger.debug("Params:")
    for route in routes:
        match, scope = route.matches(request)
        if match == Match.FULL:
            for name, value in scope["path_params"].items():
                logger.debug(f"\t{name}: {value}")
    # logger.debug("Headers:")
    # for name, value in request.headers.items():
    #     logger.debug(f"\t{name}: {value}")

    response = await call_next(request)
    return response
