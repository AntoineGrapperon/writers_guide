# ❄️ Snowflake Architect

A functional web application that guides writers through the **Snowflake Method**, an iterative process for novel design created by Randy Ingermanson.

## 🚀 Getting Started

Follow these steps to run the application locally.

### 📋 Prerequisites

- **Python 3.8+**
- **pip** (Python package installer)

### 🛠️ Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/AntoineGrapperon/writers_guide.git
   cd writers_guide
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### 🏃 Running the App

Start the Streamlit server with the following command:

```bash
streamlit run app.py
```

The application will typically open automatically in your default browser at `http://localhost:8501`.

---

## ❄️ Features

- **10-Step Workflow:** Guided progression from a single sentence to a full first draft.
- **Character Dossiers:** Interactive card-based management of your cast's motivations, goals, and arcs.
- **Dynamic Scene List:** Organize and outline your novel's narrative flow.
- **Local Persistence:** Automatic saving and loading of all your novels using a local SQLite database (`snowflake.db`). 
- **Export/Import:** Download your entire novel archive as a JSON file or import existing drafts to the local database.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
