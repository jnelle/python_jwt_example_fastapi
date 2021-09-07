import time
import uuid

import pymongo
import yaml
from loguru import logger

from service1.helpers.helpers import hash_password, load_model
from service1.models.auth import UserModel

config = yaml.safe_load(open("config.yaml"))

logger.info("Service1 CLI-TOOL ")
logger.info("Please choose:")
logger.info("1 - Add Admin")
logger.info("2 - Add User")
logger.info("3 - Show all Users")
action = int(input("Action: "))

pym = pymongo.MongoClient(config["core"]["mongodb_url"])
db = pym[config["core"]["mongodb_db"]]

if action == 1:
    name = input("Name: ")
    email = input("E-Mail: ")
    password = hash_password(input("Password: "))
    token = uuid.uuid4().hex
    reg_time = time.time()
    user = UserModel(
        name=name,
        email=email,
        password=password,
        level=3,
        token=token,
        reg_time=reg_time,
    )

    db.users.insert_one(user.dict())
    logger.info(f"Your token: {token}")  # for debug
    logger.info("Finished.")

elif action == 2:
    name = input("Name: ")
    email = input("E-Mail: ")
    password = hash_password(input("Password: "))
    token = uuid.uuid4().hex
    reg_time = time.time()
    user = UserModel(
        name=name,
        email=email,
        password=password,
        level=2,
        token=token,
        reg_time=reg_time,
    )

    db.users.insert_one(user.dict())
    logger.info(f"Your token: {token}")
    logger.info("Finished.")

elif action == 3:
    users = db.users.find()

    for user in users:
        user = load_model(UserModel, user)
        logger.info(" --- name: " + user.name)
        logger.info(" - email: " + user.email)
        logger.info(" - level: " + str(user.level))
        logger.info(" - registration date: " + str(user.reg_time))
        logger.info(" - token: " + user.token)
