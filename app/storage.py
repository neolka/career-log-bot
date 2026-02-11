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
            content = f.read().strip()
            if not content:
                return {}
            data = json.loads(content)
            
            # ВАЖЛИВА ПЕРЕВІРКА:
            if not isinstance(data, dict):
                logger.warning(f"Expected dict in users.json, got {type(data)}. Resetting to empty dict.")
                return {}
            return data
    except Exception as e:
        logger.warning(f"Error loading users.json: {e}")
        return {}
    

def _save_users(data: dict) -> None:
    if not isinstance(data, dict):
        logger.error(f"Attempted to save invalid data type to users.json: {type(data)}")
        return 
    
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving users.json: {e}")


def get_user_language(user_id: int) -> str:
    users = _load_users()
    user_info = users.get(str(user_id))
    
    if isinstance(user_info, dict):
        return user_info.get("language", "en")
    
    return "en" # Мова за замовчуванням


def set_user_language(user_id: int, lang: str) -> None:
    users = _load_users()
    
    # 2. Оновлюємо або створюємо запис для конкретного юзера
    user_key = str(user_id)
    if user_key not in users:
        users[user_key] = {}
    
    users[user_key]["language"] = lang
    
    # 3. Зберігаємо оновлений словник назад у файл
    try:
        _save_users(users)
        logger.info(f"Language for user {user_id} set to {lang}")
    except Exception as e:
        logger.error(f"Failed to save user language: {e}")
