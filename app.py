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

# Placeholder for other steps
else:
    st.header(step)
    st.write("This section is currently under construction for the Proof of Concept.")

# PBI-S.5: Snapshot & Import
st.sidebar.divider()

# Export
if st.sidebar.button("💾 Export Draft (JSON)"):
    st.sidebar.json(st.session_state.novel_data)

# Import
uploaded_file = st.sidebar.file_uploader("📂 Import Draft (JSON)", type="json")
if uploaded_file is not None:
    import json
    try:
        imported_data = json.load(uploaded_file)
        # Basic validation: check for required keys
        if all(key in imported_data for key in ['step1_hook', 'step2_summary', 'characters']):
            st.session_state.novel_data = imported_data
            st.sidebar.success("✅ Data imported successfully!")
            # Note: streamlit will rerun the script automatically on state change
        else:
            st.sidebar.error("❌ Invalid JSON format. Missing required fields.")
    except Exception as e:
        st.sidebar.error(f"❌ Error loading JSON: {e}")
