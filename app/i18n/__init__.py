from app.i18n.ua import TEXTS as UA_TEXTS
from app.i18n.en import TEXTS as EN_TEXTS

LANGUAGES = {
    "ua": UA_TEXTS,
    "en": EN_TEXTS,
}

DEFAULT_LANG = "en"
CURRENT_LANG = DEFAULT_LANG

def get_lang() -> str:
    return CURRENT_LANG


def set_lang(lang: str) -> None:
    global CURRENT_LANG
    if lang in LANGUAGES:
        CURRENT_LANG = lang
        

def t(key: str, lang: str ) -> str:
    texts = LANGUAGES.get(lang, LANGUAGES["en"])
    value = texts.get(key)

    if value is None:
        raise KeyError(f"Missing i18n key: '{key}' for lang='{lang}'")
    
    if not isinstance(value, str):
        raise TypeError(
            f"i18n key '{key}' must be str, got {type(value)}"
        )
    
    return value
