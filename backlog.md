# Product Backlog: "The Architect's Ledger" (Streamlit PoC)

## Epic: Streamlit Snowflake PoC (The "Rapid Sprout")
**Goal:** Build a functional, in-memory web app that guides a writer through the complete 10-step Snowflake method.

- [x] **PBI-S.1: Foundation & Session State**
- [x] **PBI-S.2: Step 1 - The "Hook" (Sentence Expansion)**
- [x] **PBI-S.3: Step 2 - The "Sprout" (Paragraph expansion)**
- [x] **PBI-S.4: Step 3 - Character Dossiers (The "Cast")**
- [x] **PBI-S.5: Snapshot & Export**
- [x] **PBI-S.6: Step 4 - The One-Page Summary**
- [x] **PBI-S.7: Step 5 - Character Synopses**
- [x] **PBI-S.8: Step 6 - The Four-Page Summary**
- [x] **PBI-S.9: Step 7 - Character Charts**
- [x] **PBI-S.10: Step 8 - The Scene List**
- [x] **PBI-S.11: Step 9 - The Narrative Outline**
- [x] **PBI-S.12: Step 10 - The First Draft**

## Refinements & Enhancements

- [x] **PBI-S.13: Step 3 Refinement - Character Cards**
    - UI: Replace `st.data_editor` in Step 3 with a grid of editable character cards.
    - UX: Individual "Add Character" and "Delete" actions for better control.
    - Layout: Clearer grouping of Motivation, Goal, Conflict, and Epiphany for each character.

- [x] **PBI-S.14: Step 8 Refinement - Narrative Scene Cards**
    - UI: Replace the scene table with 5 expanders corresponding to Step 6 sections.
    - UX: Add "Scene Cards" within each expander with POV and Location fields.
    - Context: Display the relevant Step 6 expansion text inside each section for reference.
    - Management: Add buttons to reorder scenes or move them between sections.

- [x] **PBI-S.15: Step 8/9 Synchronization - Scene Reordering Fix**
    - Bug Fix: Ensure reordering in Step 8 is reflected in Step 9 and Step 10.
    - Implementation: Add unique IDs to scenes and sort by narrative section in all downstream steps.
    - UX: Add explicit "Move Up/Down" buttons for scenes within Step 8.

---
*Note: This backlog is for the Streamlit implementation branch.*
