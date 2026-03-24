# Localization Strategy: Snowflake Architect

To make **Snowflake Architect** accessible to a global audience, we will implement a flexible localization (L10n) system.

## 🛠️ Technical Approach

### 1. Translation Format (JSON)
We will use JSON files stored in a `locales/` directory. JSON is easy to read, edit, and parse in Python.
- `locales/en.json` (English - Default)
- `locales/fr.json` (French)
- `locales/es.json` (Spanish)

Example structure:
```json
{
  "sidebar": {
    "title": "❄️ Snowflake Architect",
    "nav_header": "📖 My Novels",
    "steps": [
        "🏠 Home",
        "1. The One-Sentence Hook",
        ...
    ]
  },
  "home": {
    "welcome": "Welcome to: {novel_name}",
    "intro": "Writing a novel is hard..."
  }
}
```

### 2. Localization Helper (`i18n.py`)
A dedicated module will handle:
- **State Management:** Reading/Writing the selected language to `st.session_state`.
- **Loading:** Fetching the correct JSON file based on the selection.
- **Lookup Function:** A `t(key)` function (or similar) to retrieve strings.
- **Interpolation:** Support for variables in strings (e.g., `t("home.welcome", novel_name="My Book")`).

### 3. Implementation Workflow
1.  **Extract Strings:** Move hardcoded strings from `app.py` into `locales/en.json`.
2.  **Refactor Sidebar:** Add a language selection dropdown.
3.  **Refactor Steps:** Update the step list and page headers to use translated keys.
4.  **Database Migration (Optional):** Ensure that system-generated default titles (like "My First Novel") can be localized.

## 🚀 Phase 1: Proof of Concept
- Create `locales/en.json` and `locales/fr.json`.
- Implement `i18n.py`.
- Localize the **Home Page** and the **Sidebar Navigation**.

## 🌍 Why this strategy?
- **Maintainability:** Adding a new language is as simple as creating a new JSON file.
- **Streamlit Friendly:** Works perfectly with Streamlit's reactive model.
- **Performance:** JSON files are small and fast to load into memory.
