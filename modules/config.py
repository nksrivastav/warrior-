import os
import aiohttp
from os import getenv
from dotenv import load_dotenv
    
load_dotenv()
que = {}
admins = {}

API_ID = int(getenv("API_ID", "7639910"))
API_HASH = getenv("API_HASH", "d07f2a4b3ddd7f3535653773f27b777d")
BOT_TOKEN = getenv("BOT_TOKEN", "5119750402:AAGyvMmNz9vicQGqbalcGAvxszfnyv8eb6I")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "300"))
STRING_SESSION = getenv("STRING_SESSION", "BQCdBUVBRE1EgR2GCB89z77xjSVYlAPDmzlti7dS5LDuEY6Tbat_hNJthMqCmuXvtGB1ZGx-c199aeoO3vF7j3rY7bxWa8g6J3QI4BKCzT99ySCh1QtbYJKmrVJVs4Cofk_GD5jPSn8rdwFs27qgZzzEFksKSotsZWcTTAvRMNbEE-MWTWXZ0NWscgUf8SnWfq5C9sv-kpKLrHR2N7AjJzOWQJ_R1JogFgzjk2JJ6WthGnywDSd1PoPkuJk1u_KmnRId0nXKqj_60pgMQu2cyGrpNJQiYIkOA8irzkCcfLT-AMfDX7n9SYJvvXH0CBfOeK2sxknzy9XWIvx-c8Nw9lVFdbvTKAA")
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "5241878797").split()))
aiohttpsession = aiohttp.ClientSession()
