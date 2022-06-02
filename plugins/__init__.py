__version__ = "2.0"

import time
import logging
from modules import me_bot

logging.basicConfig(
  filename=f'streambot-logs-{me_bot.id}.txt',
  level=logging.INFO,
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("yt_dlp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("PyTgCalls").setLevel(logging.ERROR)

LOGS = logging.getLogger(__name__)
