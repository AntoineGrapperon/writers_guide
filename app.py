import streamlit as st
import pandas as pd

# PBI-S.1: Session State Initialization
if 'novel_data' not in st.session_state:
    st.session_state.novel_data = {
        'step1_hook': "",
        'step2_summary': "",
        'characters': [],
    }

# Sidebar Navigation
st.sidebar.title("❄️ Snowflake Architect")
step = st.sidebar.radio(
    "Go to Step:",
    [
        "1. The One-Sentence Hook",
        "2. The One-Paragraph Summary",
        "3. Character Dossiers",
        "4. The One-Page Summary",
        "5. Character Synopses",
        "6. The Four-Page Summary",
        "7. Character Charts",
        "8. The Scene List",
        "9. The Narrative Outline",
        "10. The First Draft"
    ]
)

# Step 1: The One-Sentence Hook (PBI-S.2)
if step == "1. The One-Sentence Hook":
    st.header("Step 1: The One-Sentence Hook")
    st.info("Write a single sentence that summarizes your novel. Aim for less than 15 words and avoid character names.")

    # Input
    hook = st.text_input(
        "Enter your hook:",
        value=st.session_state.novel_data['step1_hook'],
        placeholder="e.g., A scientist discovers a way to communicate with trees, but they only want to complain."
    )

    # Logic: Word count
    word_count = len(hook.split()) if hook else 0
    st.write(f"**Word Count:** {word_count} / 15")

    # Validation
    if word_count > 15:
        st.warning("⚠️ Your hook is a bit long! Try to keep it under 15 words for maximum impact.")
    elif 0 < word_count <= 15:
        st.success("✅ Great! This is a concise and powerful hook.")

    # Save to state
    st.session_state.novel_data['step1_hook'] = hook

# Step 2: The One-Paragraph Summary (PBI-S.3)
elif step == "2. The One-Paragraph Summary":
    st.header("Step 2: The One-Paragraph Summary")
    
    st.markdown("""
    Expand your one-sentence hook into a full paragraph consisting of **five sentences**:
    1.  **Setup:** Introduction of the story and characters.
    2.  **Disaster 1:** The first major conflict or setback.
    3.  **Disaster 2:** The conflict escalates.
    4.  **Disaster 3:** The climax or turning point.
    5.  **Ending:** The resolution.
    """)

    with st.expander("ℹ️ Why this structure?", expanded=True):
        st.info("This 'Three Disasters + Ending' structure ensures your story has rising tension and a clear arc from the very beginning.")

    # Input
    summary = st.text_area(
        "Draft your summary:",
        value=st.session_state.novel_data['step2_summary'],
        height=200,
        placeholder="Sentence 1 (Setup)... Sentence 2 (Disaster 1)... Sentence 3 (Disaster 2)... Sentence 4 (Disaster 3)... Sentence 5 (Ending)..."
    )

    # Logic: Sentence count (approximate)
    sentence_count = len([s for s in summary.split('.') if s.strip()]) if summary else 0
    st.write(f"**Sentence Count:** {sentence_count} / 5")

    # Validation
    if sentence_count == 5:
        st.success("✅ Perfect structure! You have exactly 5 sentences.")
    elif sentence_count > 5:
        st.warning("⚠️ You have more than 5 sentences. Try to combine ideas to keep it punchy.")
    elif 0 < sentence_count < 5:
        st.info(f"You have {sentence_count} sentences. Keep going until you hit 5!")

    # Save to state
    st.session_state.novel_data['step2_summary'] = summary

# Step 3: Character Dossiers (PBI-S.4)
elif step == "3. Character Dossiers":
    st.header("Step 3: Character Dossiers")
    st.markdown("""
    Every story is driven by its characters. For each of your major characters, define the following:
    *   **Motivation:** What do they want abstractly?
    *   **Goal:** What is their concrete objective?
    *   **Conflict:** What prevents them from reaching that goal?
    *   **Epiphany:** What do they learn or how do they change?
    """)

    # Initialize dataframe-friendly list if empty
    if not st.session_state.novel_data['characters']:
        # Add a placeholder character to guide the user
        st.session_state.novel_data['characters'] = [
            {"Name": "Protagonist", "Motivation": "", "Goal": "", "Conflict": "", "Epiphany": ""}
        ]

    # Use st.data_editor for a spreadsheet-like experience
    edited_df = st.data_editor(
        pd.DataFrame(st.session_state.novel_data['characters']),
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Name": st.column_config.TextColumn("Character Name", width="medium", help="The name of your character"),
            "Motivation": st.column_config.TextColumn("Motivation (Abstract Want)", width="large"),
            "Goal": st.column_config.TextColumn("Goal (Concrete Objective)", width="large"),
            "Conflict": st.column_config.TextColumn("Conflict (The Obstacle)", width="large"),
            "Epiphany": st.column_config.TextColumn("Epiphany (Lesson Learned)", width="large"),
        }
    )

    # Save changes back to session state
    st.session_state.novel_data['characters'] = edited_df.to_dict('records')
    
    st.info("💡 You can add new rows by clicking the '+' at the bottom of the table.")

# Step 4: The One-Page Summary
elif step == "4. The One-Page Summary":
    st.header("Step 4: The One-Page Summary")
    st.markdown("""
    Expand each of your five sentences from **Step 2** into a full paragraph. 
    *   The first four paragraphs should end in a **disaster**.
    *   The final paragraph should tell the **resolution**.
    """)

    # Initialize step 4 data if not present
    if 'step4_paragraphs' not in st.session_state.novel_data:
        st.session_state.novel_data['step4_paragraphs'] = ["", "", "", "", ""]

    # Get Step 2 sentences to use as prompts
    step2_text = st.session_state.novel_data['step2_summary']
    sentences = [s.strip() + "." for s in step2_text.split('.') if s.strip()]
    
    # Ensure we have 5 prompts
    prompts = sentences + ["(No summary provided in Step 2)"] * (5 - len(sentences))

    labels = ["1. Setup", "2. Disaster 1", "3. Disaster 2", "4. Disaster 3", "5. Ending"]
    
    updated_paragraphs = []
    for i in range(5):
        st.subheader(labels[i])
        st.caption(f"Prompt: {prompts[i]}")
        para = st.text_area(
            f"Paragraph {i+1}",
            value=st.session_state.novel_data['step4_paragraphs'][i],
            height=150,
            key=f"para_{i}"
        )
        updated_paragraphs.append(para)

    st.session_state.novel_data['step4_paragraphs'] = updated_paragraphs

# Placeholder for other steps
else:
    st.header(step)
    st.write("This section is currently under construction for the Proof of Concept.")

# PBI-S.5: Snapshot & Import
st.sidebar.divider()

# Export
import json
json_data = json.dumps(st.session_state.novel_data, indent=2)
st.sidebar.download_button(
    label="💾 Download Draft (JSON)",
    data=json_data,
    file_name="snowflake_draft.json",
    mime="application/json"
)

# Import
uploaded_file = st.sidebar.file_uploader("📂 Import Draft (JSON)", type="json")
if uploaded_file is not None:
    try:
        imported_data = json.load(uploaded_file)
        # Basic validation: check for core required keys
        required_keys = ['step1_hook', 'step2_summary', 'characters']
        if all(key in imported_data for key in required_keys):
            st.session_state.novel_data = imported_data
            st.sidebar.success("✅ Data imported successfully!")
        else:
            st.sidebar.error("❌ Invalid JSON format. Missing required fields.")
    except Exception as e:
        st.sidebar.error(f"❌ Error loading JSON: {e}")
