# Product Backlog: "The Architect's Ledger" (Streamlit PoC)

## Epic: Streamlit Snowflake PoC (The "Rapid Sprout")
**Goal:** Build a functional, in-memory web app that guides a writer through the first three steps of the Snowflake method.

- [x] **PBI-S.1: Foundation & Session State**
    - Setup: Create `requirements.txt` with `streamlit` and `pandas`.
    - State Initialization: Implement a robust `st.session_state` schema.
    - Sidebar Navigation: Create a persistent sidebar for 10 Snowflake steps.
- [x] **PBI-S.2: Step 1 - The "Hook" (Sentence Expansion)**
    - UI: Page for Step 1 with live word counter.
    - Validation: Visual feedback for the 15-word constraint.
- [ ] **PBI-S.3: Step 2 - The "Sprout" (Paragraph expansion)**
    - UI: Text area for the 5-sentence summary.
    - Guideline helper: Display the "3 disasters + 1 ending" structure.
- [ ] **PBI-S.4: Step 3 - Character Dossiers (The "Cast")**
    - UI: Interface to CRUD (Create, Read, Update, Delete) characters.
    - Data Entry: Capture Name, Motivation, Goal, Conflict, and Epiphany.
- [ ] **PBI-S.5: Snapshot & Export**
    - Logic: Consolidate session state into JSON/Markdown format.
    - UI: "Download My Novel Architecture" button.

---
*Note: This backlog is for the Streamlit implementation branch.*
