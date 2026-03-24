import json
import streamlit as st
import os

DEFAULT_LANG = "en"
SUPPORTED_LANGS = ["en", "fr", "es"]

def load_translations(lang):
    """Load JSON translation file."""
    path = f"locales/{lang}.json"
    if not os.path.exists(path):
        path = f"locales/{DEFAULT_LANG}.json"
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_text(key, **kwargs):
    """Retrieve translated text by key."""
    if "translations" not in st.session_state:
        st.session_state.translations = load_translations(st.session_state.get("lang", DEFAULT_LANG))
    
    # Traverse nested keys (e.g., "sidebar.title")
    keys = key.split(".")
    data = st.session_state.translations
    for k in keys:
        if isinstance(data, dict) and k in data:
            data = data[k]
        else:
            return key # Fallback to key if not found
    
    if isinstance(data, str):
        return data.format(**kwargs)
    return data

def init_i18n():
    """Initialize language settings in session state."""
    if "lang" not in st.session_state:
        st.session_state.lang = DEFAULT_LANG
    
    if "translations" not in st.session_state:
        st.session_state.translations = load_translations(st.session_state.lang)

def change_lang(new_lang):
    """Update language and reload translations."""
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.session_state.translations = load_translations(new_lang)
        st.rerun()
