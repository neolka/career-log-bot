import json
from datetime import datetime
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

FILE_PATH = Path("data/achievements.json")


def load_achievements():
    if not FILE_PATH.exists():
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning("Achievements file not found or invalid")
        return []


def save_achievement(answers: list[str]):
    achievement = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "context": answers[0],
        "action": answers[1],
        "result": answers[2],
    }

    data = load_achievements()
    data.append(achievement)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info("Achievement successfully saved")


    
