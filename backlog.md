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
- [x] **PBI-S.3: Step 2 - The "Sprout" (Paragraph expansion)**
    - UI: Text area for the 5-sentence summary.
    - Guideline helper: Display the "3 disasters + 1 ending" structure.
- [x] **PBI-S.4: Step 3 - Character Dossiers (The "Cast")**
    - UI: Interface to CRUD (Create, Read, Update, Delete) characters.
    - Data Entry: Capture Name, Motivation, Goal, Conflict, and Epiphany.
- [x] **PBI-S.5: Snapshot & Export**
    - Logic: Consolidate session state into JSON format.
    - UI: "Download My Novel Architecture" button and "Import JSON" uploader.
- [x] **PBI-S.6: Step 4 - The One-Page Summary**
    - UI: 5 text areas for expanding Step 2 sentences into paragraphs.
    - Context: Display Step 2 sentences as prompts for expansion.
- [x] **PBI-S.7: Step 5 - Character Synopses**
    - UI: Dynamic list of text areas for each character defined in Step 3.
    - Context: Display Step 3 character traits (Motivation/Goal/Conflict) as reference.

---
*Note: This backlog is for the Streamlit implementation branch.*
