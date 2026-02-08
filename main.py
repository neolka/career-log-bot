# main.py
from app.bot import run_bot
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("BOT STARTED")
    run_bot()
