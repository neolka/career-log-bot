from app.i18n.ua import TEXTS as UA_TEXTS
from app.i18n.en import TEXTS as EN_TEXTS
from app.storage import get_user_language, set_user_language
import logging

logger = logging.getLogger(__name__)

LANGUAGES = {
    "ua": UA_TEXTS,
    "en": EN_TEXTS,
}

DEFAULT_LANG = "en"

def get_lang(user_id: int) -> str:
    return get_user_language(user_id)


def set_lang(user_id: int, lang: str) -> None:
    if lang in LANGUAGES:
        set_user_language(user_id, lang)
        

def t(key: str, lang: str) -> str:
    texts = LANGUAGES.get(lang, LANGUAGES["en"])
    value = texts.get(key)

    if value is None:
        logger.error(f"Missing i18n key: '{key}' for lang='{lang}'")
        return key
    
    if not isinstance(value, str):
        logger.warning(f"i18n key '{key}' is not a string, converting...")
        return str(value)
    
    return value
