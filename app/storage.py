import json
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

ACHIEVEMENTS_FILE = Path("data/achievements.json")
USERS_FILE = Path("data/users.json")

def load_achievements() -> list[dict]:
    if not ACHIEVEMENTS_FILE.exists():
        return []

    try:
        with open(ACHIEVEMENTS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning("Achievements file not found or invalid")
        return []

def save_achievement(answers: list[str]) -> None:
    achievement = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "context": answers[0],
        "action": answers[1],
        "result": answers[2],
    }

    data = load_achievements()
    data.append(achievement)

    with open(ACHIEVEMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info("Achievement successfully saved")

def _load_users() -> dict:
    if not USERS_FILE.exists():
        return {}

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        logger.warning("Invalid users.json")
        return {}

def _save_users(data: dict) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_user_language(user_id: int) -> str:
    users = _load_users()
    return users.get(str(user_id), {}).get("language", "en")

def set_user_language(user_id: int, lang: str) -> None:
    users = _load_users()
    users.setdefault(str(user_id), {})["language"] = lang
    _save_users(users)
