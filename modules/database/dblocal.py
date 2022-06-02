""" mongo database """

from motor.motor_asyncio import AsyncIOMotorClient as Bot
from modules.config import MONGODB_URL as tmo


MONGODB_CLI = Bot(tmo)
db = MONGODB_CLI.program
