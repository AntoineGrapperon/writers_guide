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

# Placeholder for other steps
else:
    st.header(step)
    st.write("This section is currently under construction for the Proof of Concept.")
    if step == "2. The One-Paragraph Summary":
        st.info("Coming soon: PBI-S.3")
    elif step == "3. Character Dossiers":
        st.info("Coming soon: PBI-S.4")

# PBI-S.5: Snapshot (Draft)
st.sidebar.divider()
if st.sidebar.button("💾 Export Draft (JSON)"):
    st.sidebar.json(st.session_state.novel_data)
