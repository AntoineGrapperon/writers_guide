import streamlit as st
import pandas as pd

# PBI-S.1: Session State Initialization
if 'novel_data' not in st.session_state:
    st.session_state.novel_data = {
        'step1_hook': "",
        'step2_summary': "",
        'characters': [],
        'step4_paragraphs': ["", "", "", "", ""],
        'character_synopses': {},
        'step6_pages': ["", "", "", "", ""],
        'character_charts': {},
        'scene_list': [],
        'scene_outlines': {},
        'scene_content': {},
    }

# Sidebar Navigation
st.sidebar.title("❄️ Snowflake Architect")
step = st.sidebar.radio(
    "Go to Step:",
    [
        "🏠 Home",
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

# Home Page content
if step == "🏠 Home":
    st.header("🏠 Welcome to Snowflake Architect")
    st.markdown("""
    Writing a novel is hard. The **Snowflake Method**, created by Randy Ingermanson, makes it manageable by starting with a small "snowflake" of an idea and expanding it into a complete story.

    ### ❄️ What is the Snowflake Method?
    Instead of starting from page one and hoping for the best (the "Pantser" approach), the Snowflake Method is a "Plotter" strategy. You begin with a single sentence and systematically grow it into a full-length manuscript through ten structured steps.

    ### 🛠️ How to use this tool:
    1.  **Iterative Growth:** Each step builds upon the work you did in the previous one. 
    2.  **Character & Plot:** You'll alternate between developing your story's plot and deepening your characters.
    3.  **Flexibility:** Don't be afraid to go back to earlier steps! If you discover something new about a character in Step 5, update Step 1 to match.
    4.  **Save Your Progress:** Use the **Download Draft** button in the sidebar to save your work locally. You can resume later by using the **Import Draft** button.

    ### 🚀 Getting Started:
    Select **"1. The One-Sentence Hook"** from the sidebar to begin your journey!
    """)

# Step 1: The One-Sentence Hook (PBI-S.2)
elif step == "1. The One-Sentence Hook":
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

# Step 5: Character Synopses
elif step == "5. Character Synopses":
    st.header("Step 5: Character Synopses")
    st.markdown("""
    Write a one-page synopsis for each of your major characters. 
    These synopses should tell the story **from that character's point of view**.
    """)

    characters = st.session_state.novel_data.get('characters', [])
    
    if not characters or (len(characters) == 1 and characters[0]['Name'] == "Protagonist" and not characters[0]['Motivation']):
        st.warning("⚠️ No characters found. Please go to **Step 3: Character Dossiers** to add your cast first.")
    else:
        # Initialize synopses dictionary if not present
        if 'character_synopses' not in st.session_state.novel_data:
            st.session_state.novel_data['character_synopses'] = {}

        for char in characters:
            name = char.get('Name', 'Unnamed Character')
            if not name: continue
            
            with st.expander(f"📖 POV Synopsis: {name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write("**Reference (Step 3):**")
                    st.write(f"**Motivation:** {char.get('Motivation', 'N/A')}")
                    st.write(f"**Goal:** {char.get('Goal', 'N/A')}")
                    st.write(f"**Conflict:** {char.get('Conflict', 'N/A')}")
                
                with col2:
                    current_synopsis = st.session_state.novel_data['character_synopses'].get(name, "")
                    new_synopsis = st.text_area(
                        f"Synopsis for {name}",
                        value=current_synopsis,
                        height=250,
                        key=f"synopsis_{name}",
                        label_visibility="collapsed"
                    )
                    st.session_state.novel_data['character_synopses'][name] = new_synopsis

# Step 6: The Four-Page Summary
elif step == "6. The Four-Page Summary":
    st.header("Step 6: The Four-Page Summary")
    st.markdown("""
    Expand your one-page summary into a much more detailed narrative. 
    In the full Snowflake method, this would be about four pages of text.
    """)

    # Initialize step 6 data if not present
    if 'step6_pages' not in st.session_state.novel_data:
        st.session_state.novel_data['step6_pages'] = ["", "", "", "", ""]

    # Get Step 4 paragraphs to use as prompts
    step4_paras = st.session_state.novel_data.get('step4_paragraphs', ["", "", "", "", ""])
    
    labels = ["1. Detailed Setup", "2. Disaster 1 Expansion", "3. Disaster 2 Expansion", "4. Disaster 3 Expansion", "5. Resolution Expansion"]
    
    updated_pages = []
    for i in range(5):
        st.subheader(labels[i])
        with st.expander("📄 Reference: Step 4 Paragraph", expanded=False):
            st.write(step4_paras[i] if step4_paras[i] else "*(Empty)*")
            
        page_text = st.text_area(
            f"Expansion for {labels[i]}",
            value=st.session_state.novel_data['step6_pages'][i],
            height=400,
            key=f"page_{i}",
            label_visibility="collapsed"
        )
        updated_pages.append(page_text)

    st.session_state.novel_data['step6_pages'] = updated_pages

# Step 7: Character Charts
elif step == "7. Character Charts":
    st.header("Step 7: Character Charts")
    st.markdown("""
    Deepen your characters. Flesh out their physical traits, history, and most importantly, 
    how they will change by the end of the story.
    """)

    characters = st.session_state.novel_data.get('characters', [])
    
    if not characters or (len(characters) == 1 and characters[0]['Name'] == "Protagonist" and not characters[0]['Motivation']):
        st.warning("⚠️ No characters found. Please go to **Step 3: Character Dossiers** to add your cast first.")
    else:
        # Initialize charts dictionary if not present
        if 'character_charts' not in st.session_state.novel_data:
            st.session_state.novel_data['character_charts'] = {}

        for char in characters:
            name = char.get('Name', 'Unnamed Character')
            if not name: continue
            
            # Ensure an entry exists for this character
            if name not in st.session_state.novel_data['character_charts']:
                st.session_state.novel_data['character_charts'][name] = {
                    "Age/Birth": "", "Appearance": "", "Backstory": "", "Personality": "", "Arc": ""
                }
            
            with st.expander(f"👤 Character Chart: {name}", expanded=True):
                # References
                with st.container():
                    st.caption("Step 3/5 Reference")
                    cols = st.columns(3)
                    cols[0].write(f"**Goal:** {char.get('Goal', 'N/A')}")
                    cols[1].write(f"**Conflict:** {char.get('Conflict', 'N/A')}")
                    cols[2].write(f"**Epiphany:** {char.get('Epiphany', 'N/A')}")

                chart_data = st.session_state.novel_data['character_charts'][name]
                
                c1, c2 = st.columns(2)
                chart_data["Age/Birth"] = c1.text_input("Age / Birth Date", value=chart_data.get("Age/Birth", ""), key=f"age_{name}")
                chart_data["Appearance"] = c2.text_input("Physical Appearance", value=chart_data.get("Appearance", ""), key=f"app_{name}")
                
                chart_data["Backstory"] = st.text_area("History / Backstory", value=chart_data.get("Backstory", ""), height=150, key=f"back_{name}")
                chart_data["Personality"] = st.text_area("Personality Traits", value=chart_data.get("Personality", ""), height=100, key=f"pers_{name}")
                chart_data["Arc"] = st.text_area("Character Arc (How they change)", value=chart_data.get("Arc", ""), height=200, key=f"arc_{name}")

# Step 8: The Scene List
elif step == "8. The Scene List":
    st.header("Step 8: The Scene List")
    st.markdown("""
    Break your four-page summary into a list of scenes. 
    Each scene should have a clear POV character and a specific purpose.
    """)

    # References from Step 6
    with st.expander("📄 Reference: Step 6 Detailed Narrative", expanded=False):
        step6_pages = st.session_state.novel_data.get('step6_pages', [])
        labels = ["Setup", "Disaster 1", "Disaster 2", "Disaster 3", "Resolution"]
        for label, text in zip(labels, step6_pages):
            st.write(f"**{label}:**")
            st.write(text if text else "*(Empty)*")
            st.divider()

    # Get character names for POV dropdown
    char_names = [c['Name'] for c in st.session_state.novel_data.get('characters', []) if c.get('Name')]
    if not char_names:
        char_names = ["Protagonist"]

    # Initialize scene list if empty
    if 'scene_list' not in st.session_state.novel_data or not st.session_state.novel_data['scene_list']:
        st.session_state.novel_data['scene_list'] = [
            {"Scene #": 1, "POV Character": char_names[0], "Description": "", "Location": ""}
        ]

    # Data Editor
    edited_scenes = st.data_editor(
        pd.DataFrame(st.session_state.novel_data['scene_list']),
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Scene #": st.column_config.NumberColumn("Order", width="small", min_value=1),
            "POV Character": st.column_config.SelectboxColumn("POV Character", options=char_names, width="medium"),
            "Description": st.column_config.TextColumn("What happens?", width="large"),
            "Location": st.column_config.TextColumn("Location", width="medium"),
        }
    )

    # Save to state
    st.session_state.novel_data['scene_list'] = edited_scenes.to_dict('records')
    st.info("💡 Pro-tip: Aim for 40-80 scenes for a standard-length novel.")

# Step 9: The Narrative Outline
elif step == "9. The Narrative Outline":
    st.header("Step 9: The Narrative Outline")
    st.markdown("""
    Expand each scene from your **Step 8 Scene List** into a detailed narrative outline. 
    This is your final check of the story's flow before you start writing the actual draft.
    """)

    scenes = st.session_state.novel_data.get('scene_list', [])
    
    if not scenes or (len(scenes) == 1 and not scenes[0]['Description']):
         st.warning("⚠️ No scenes found. Please go to **Step 8: The Scene List** to define your scenes first.")
    else:
        # Initialize outlines dictionary if not present
        if 'scene_outlines' not in st.session_state.novel_data:
            st.session_state.novel_data['scene_outlines'] = {}

        for scene in scenes:
            scene_num = scene.get('Scene #', '?')
            pov = scene.get('POV Character', 'Unknown')
            desc = scene.get('Description', 'No description')
            loc = scene.get('Location', 'TBD')
            
            # Key for state
            scene_id = f"scene_{scene_num}_{pov}_{desc[:20]}"
            
            with st.expander(f"🎬 Scene {scene_num}: {desc[:50]}...", expanded=True):
                st.caption(f"POV: {pov} | Location: {loc}")
                st.write(f"**Brief:** {desc}")
                
                current_outline = st.session_state.novel_data['scene_outlines'].get(scene_id, "")
                new_outline = st.text_area(
                    f"Detailed Outline for Scene {scene_num}",
                    value=current_outline,
                    height=200,
                    key=f"outline_{scene_id}",
                    label_visibility="collapsed"
                )
                st.session_state.novel_data['scene_outlines'][scene_id] = new_outline

# Step 10: The First Draft
elif step == "10. The First Draft":
    st.header("Step 10: The First Draft")
    st.markdown("""
    It's time to write! Select a scene from your outline and start drafting. 
    Your planning from previous steps is available as a reference.
    """)

    scenes = st.session_state.novel_data.get('scene_list', [])
    
    if not scenes or (len(scenes) == 1 and not scenes[0]['Description']):
        st.warning("⚠️ No scenes found. Please complete the previous steps first.")
    else:
        # Initialize content dictionary if not present
        if 'scene_content' not in st.session_state.novel_data:
            st.session_state.novel_data['scene_content'] = {}

        # Scene selection
        scene_options = [f"Scene {s['Scene #']}: {s['Description'][:30]}..." for s in scenes]
        selected_scene_idx = st.selectbox("Select a scene to write:", range(len(scene_options)), format_func=lambda x: scene_options[x])
        
        selected_scene = scenes[selected_scene_idx]
        scene_num = selected_scene.get('Scene #', '?')
        pov = selected_scene.get('POV Character', 'Unknown')
        desc = selected_scene.get('Description', '')
        
        # Key for state (consistent with Step 9)
        scene_id = f"scene_{scene_num}_{pov}_{desc[:20]}"
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📜 Reference")
            st.write(f"**POV:** {pov}")
            st.write(f"**Brief:** {desc}")
            
            with st.expander("📝 Scene Outline (Step 9)", expanded=True):
                outline = st.session_state.novel_data.get('scene_outlines', {}).get(scene_id, "*(No outline found)*")
                st.write(outline)
            
            with st.expander("👤 Character traits", expanded=False):
                charts = st.session_state.novel_data.get('character_charts', {}).get(pov, {})
                if charts:
                    st.write(f"**Appearance:** {charts.get('Appearance', 'N/A')}")
                    st.write(f"**Backstory:** {charts.get('Backstory', 'N/A')}")
                    st.write(f"**Arc:** {charts.get('Arc', 'N/A')}")
                else:
                    st.write("No character chart found for this POV.")

        with col2:
            st.subheader(f"✍️ Writing: Scene {scene_num}")
            current_prose = st.session_state.novel_data['scene_content'].get(scene_id, "")
            new_prose = st.text_area(
                "Write your prose here:",
                value=current_prose,
                height=600,
                key=f"prose_{scene_id}",
                label_visibility="collapsed"
            )
            st.session_state.novel_data['scene_content'][scene_id] = new_prose
            
            word_count = len(new_prose.split()) if new_prose else 0
            st.caption(f"Word count for this scene: {word_count}")

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
            # Merge with default state to ensure all keys exist
            new_data = {
                'step1_hook': "",
                'step2_summary': "",
                'characters': [],
                'step4_paragraphs': ["", "", "", "", ""],
                'character_synopses': {},
                'step6_pages': ["", "", "", "", ""],
                'character_charts': {},
                'scene_list': [],
                'scene_outlines': {},
                'scene_content': {},
            }
            new_data.update(imported_data)
            st.session_state.novel_data = new_data
            st.sidebar.success("✅ Data imported successfully!")
        else:
            st.sidebar.error("❌ Invalid JSON format. Missing required fields.")
    except Exception as e:
        st.sidebar.error(f"❌ Error loading JSON: {e}")
