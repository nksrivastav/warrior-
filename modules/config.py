import os
import aiohttp
from os import getenv
from dotenv import load_dotenv
    
load_dotenv()
que = {}
admins = {}

API_ID = int(getenv("API_ID", "4441263"))
API_HASH = getenv("API_HASH", "83aa7fc275ea829e5e77f13992e48fcb")
BOT_TOKEN = getenv("BOT_TOKEN", "5046865093:AAG-RdOo-vB3qh3xJsWvi1heohzWkqFLpbU")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "300"))
STRING_SESSION = getenv("STRING_SESSION", "BQDAVomRsF98XLUfvYXHCYS6H8UDXXws-euVh9X8veE7d0rewXxbCzIMcY8bWjqGyhWxHMokJ7td1P5T2vaB051PyxxEFhgLvvzNcnKbxgStlkPYsaN8xEFS3yV5HcKp2u4vtC0Hx2cnKG_7D7-pT4nk2R8ch2EsKdbtRO4kzPZz01tDBZLihzjDSuttl7S7q1_MjdVD1niN3SvRBM3w4gGd8vtuOWltoFoR4jyjA5jH5QMAtJS4KODmJIGfVjakWCQ_cx4b5CWeYFwrIYiKkNvpLxjDMMnVoeho9XuKXj-0eY3Zu2mcQabXfwb6KhbnrRQfyz3whYV60vGyIdjKJYSScTctTAA")
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "5356564375").split()))
aiohttpsession = aiohttp.ClientSession()
