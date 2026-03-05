# Product Backlog: "The Architect's Ledger" (Streamlit PoC)

## Epic: Streamlit Snowflake PoC (The "Rapid Sprout")
**Goal:** Build a functional, in-memory web app that guides a writer through the complete 10-step Snowflake method.

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
- [x] **PBI-S.8: Step 6 - The Four-Page Summary**
    - UI: 5 large text areas for expanding Step 4 paragraphs into detailed narrative sections.
    - Context: Display Step 4 paragraphs in expanders for reference.
- [x] **PBI-S.9: Step 7 - Character Charts**
    - UI: Detailed fields for each character (Age, Appearance, Backstory, Personality, Arc).
    - Context: Display Step 3/5 core traits for reference while deepening the profile.
- [x] **PBI-S.10: Step 8 - The Scene List**
    - UI: Dynamic spreadsheet using `st.data_editor` to manage the list of scenes.
    - Features: POV Character selection (from Step 3 list), order numbering, and location tracking.
    - Context: Display Step 6 narrative sections in expanders for reference.
- [x] **PBI-S.11: Step 9 - The Narrative Outline**
    - UI: List of text areas for expanding each scene from Step 8 into a detailed outline.
    - Context: Display Step 8 scene metadata (POV, Brief, Location) in expanders for reference.
- [x] **PBI-S.12: Step 10 - The First Draft**
    - UI: Focused writing interface with scene selection.
    - Context: Side-by-side view of the Step 9 outline and character charts while drafting prose.

- [x] **PBI-S.13: Step 3 Refinement - Character Cards**
    - UI: Replace `st.data_editor` in Step 3 with a grid of editable character cards.
    - UX: Individual "Add Character" and "Delete" actions for better control.
    - Layout: Clearer grouping of Motivation, Goal, Conflict, and Epiphany for each character.

---
*Note: This backlog is for the Streamlit implementation branch.*
