import streamlit as st
import pandas as pd
import json
import uuid
import db

# Helper to create a new novel structure
def create_empty_novel():
    return {
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

# PBI-S.1: Database-backed Session State Initialization
if 'novels' not in st.session_state:
    db.init_db()
    st.session_state.novels = db.load_all_novels()
    
    # Ensure at least one novel exists
    if not st.session_state.novels:
        st.session_state.novels = {"My First Novel": create_empty_novel()}
        db.save_novel("My First Novel", st.session_state.novels["My First Novel"])

if 'current_novel' not in st.session_state:
    st.session_state.current_novel = list(st.session_state.novels.keys())[0]

# Shortcut for the current novel data
novel_data = st.session_state.novels[st.session_state.current_novel]

# Sidebar Navigation
st.sidebar.title("❄️ Snowflake Architect")

# Project Manager
st.sidebar.divider()
st.sidebar.subheader("📖 My Novels")

# Select Novel
novel_list = list(st.session_state.novels.keys())
current_idx = novel_list.index(st.session_state.current_novel) if st.session_state.current_novel in novel_list else 0
selected_novel = st.sidebar.selectbox("Active Novel:", novel_list, index=current_idx)

if selected_novel != st.session_state.current_novel:
    st.session_state.current_novel = selected_novel
    st.rerun()

# Add New Novel
with st.sidebar.expander("➕ New Novel"):
    new_novel_name = st.text_input("Novel Title", key="new_novel_name")
    if st.button("Create"):
        if new_novel_name and new_novel_name not in st.session_state.novels:
            st.session_state.novels[new_novel_name] = create_empty_novel()
            db.save_novel(new_novel_name, st.session_state.novels[new_novel_name])
            st.session_state.current_novel = new_novel_name
            st.rerun()
        elif new_novel_name:
            st.error("Title already exists!")

# Delete Novel
if len(st.session_state.novels) > 1:
    if st.sidebar.button("🗑️ Delete Current Novel"):
        old_name = st.session_state.current_novel
        del st.session_state.novels[old_name]
        db.delete_novel(old_name)
        st.session_state.current_novel = list(st.session_state.novels.keys())[0]
        st.rerun()

st.sidebar.divider()

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
    st.header(f"🏠 Welcome to: {st.session_state.current_novel}")
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
        value=novel_data['step1_hook'],
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
    novel_data['step1_hook'] = hook

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
        value=novel_data['step2_summary'],
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
    novel_data['step2_summary'] = summary

# Step 3: Character Dossiers (PBI-S.13)
elif step == "3. Character Dossiers":
    st.header("Step 3: Character Dossiers")
    st.markdown("""
    Every story is driven by its characters. For each of your major characters, define the following:
    *   **Motivation:** What do they want abstractly?
    *   **Goal:** What is their concrete objective?
    *   **Conflict:** What prevents them from reaching that goal?
    *   **Epiphany:** What do they learn or how do they change?
    """)

    # Initialize list if empty
    if not novel_data['characters']:
        novel_data['characters'] = [
            {"Name": "Protagonist", "Motivation": "", "Goal": "", "Conflict": "", "Epiphany": ""}
        ]

    # Display characters as cards
    for i, char in enumerate(novel_data['characters']):
        with st.container(border=True):
            col_header, col_delete = st.columns([5, 1])
            
            with col_header:
                # Update name directly in session state
                novel_data['characters'][i]['Name'] = st.text_input(
                    "Character Name", 
                    value=char['Name'], 
                    key=f"char_name_{i}",
                    label_visibility="collapsed"
                )
            
            with col_delete:
                if st.button("🗑️", key=f"del_char_{i}", help="Delete this character"):
                    novel_data['characters'].pop(i)
                    st.rerun()

            c1, c2 = st.columns(2)
            with c1:
                novel_data['characters'][i]['Motivation'] = st.text_area(
                    "Motivation (Abstract Want)", 
                    value=char['Motivation'], 
                    key=f"char_mot_{i}", 
                    height=100
                )
                novel_data['characters'][i]['Goal'] = st.text_area(
                    "Goal (Concrete Objective)", 
                    value=char['Goal'], 
                    key=f"char_goal_{i}", 
                    height=100
                )
            with c2:
                novel_data['characters'][i]['Conflict'] = st.text_area(
                    "Conflict (The Obstacle)", 
                    value=char['Conflict'], 
                    key=f"char_conf_{i}", 
                    height=100
                )
                novel_data['characters'][i]['Epiphany'] = st.text_area(
                    "Epiphany (Lesson Learned)", 
                    value=char['Epiphany'], 
                    key=f"char_epi_{i}", 
                    height=100
                )

    if st.button("➕ Add Character"):
        novel_data['characters'].append(
            {"Name": f"Character {len(novel_data['characters']) + 1}", "Motivation": "", "Goal": "", "Conflict": "", "Epiphany": ""}
        )
        st.rerun()

# Step 4: The One-Page Summary
elif step == "4. The One-Page Summary":
    st.header("Step 4: The One-Page Summary")
    st.markdown("""
    Expand each of your five sentences from **Step 2** into a full paragraph. 
    *   The first four paragraphs should end in a **disaster**.
    *   The final paragraph should tell the **resolution**.
    """)

    # Initialize step 4 data if not present
    if 'step4_paragraphs' not in novel_data:
        novel_data['step4_paragraphs'] = ["", "", "", "", ""]

    # Get Step 2 sentences to use as prompts
    step2_text = novel_data['step2_summary']
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
            value=novel_data['step4_paragraphs'][i],
            height=150,
            key=f"para_{i}"
        )
        updated_paragraphs.append(para)

    novel_data['step4_paragraphs'] = updated_paragraphs

# Step 5: Character Synopses
elif step == "5. Character Synopses":
    st.header("Step 5: Character Synopses")
    st.markdown("""
    Write a one-page synopsis for each of your major characters. 
    These synopses should tell the story **from that character's point of view**.
    """)

    characters = novel_data.get('characters', [])
    
    if not characters or (len(characters) == 1 and characters[0]['Name'] == "Protagonist" and not characters[0]['Motivation']):
        st.warning("⚠️ No characters found. Please go to **Step 3: Character Dossiers** to add your cast first.")
    else:
        # Initialize synopses dictionary if not present
        if 'character_synopses' not in novel_data:
            novel_data['character_synopses'] = {}

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
                    current_synopsis = novel_data['character_synopses'].get(name, "")
                    new_synopsis = st.text_area(
                        f"Synopsis for {name}",
                        value=current_synopsis,
                        height=250,
                        key=f"synopsis_{name}",
                        label_visibility="collapsed"
                    )
                    novel_data['character_synopses'][name] = new_synopsis

# Step 6: The Four-Page Summary
elif step == "6. The Four-Page Summary":
    st.header("Step 6: The Four-Page Summary")
    st.markdown("""
    Expand your one-page summary into a much more detailed narrative. 
    In the full Snowflake method, this would be about four pages of text.
    """)

    # Initialize step 6 data if not present
    if 'step6_pages' not in novel_data:
        novel_data['step6_pages'] = ["", "", "", "", ""]

    # Get Step 4 paragraphs to use as prompts
    step4_paras = novel_data.get('step4_paragraphs', ["", "", "", "", ""])
    
    labels = ["1. Detailed Setup", "2. Disaster 1 Expansion", "3. Disaster 2 Expansion", "4. Disaster 3 Expansion", "5. Resolution Expansion"]
    
    updated_pages = []
    for i in range(5):
        st.subheader(labels[i])
        with st.expander("📄 Reference: Step 4 Paragraph", expanded=False):
            st.write(step4_paras[i] if step4_paras[i] else "*(Empty)*")
            
        page_text = st.text_area(
            f"Expansion for {labels[i]}",
            value=novel_data['step6_pages'][i],
            height=400,
            key=f"page_{i}",
            label_visibility="collapsed"
        )
        updated_pages.append(page_text)

    novel_data['step6_pages'] = updated_pages

# Step 7: Character Charts
elif step == "7. Character Charts":
    st.header("Step 7: Character Charts")
    st.markdown("""
    Deepen your characters. Flesh out their physical traits, history, and most importantly, 
    how they will change by the end of the story.
    """)

    characters = novel_data.get('characters', [])
    
    if not characters or (len(characters) == 1 and characters[0]['Name'] == "Protagonist" and not characters[0]['Motivation']):
        st.warning("⚠️ No characters found. Please go to **Step 3: Character Dossiers** to add your cast first.")
    else:
        # Initialize charts dictionary if not present
        if 'character_charts' not in novel_data:
            novel_data['character_charts'] = {}

        for char in characters:
            name = char.get('Name', 'Unnamed Character')
            if not name: continue
            
            # Ensure an entry exists for this character
            if name not in novel_data['character_charts']:
                novel_data['character_charts'][name] = {
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

                chart_data = novel_data['character_charts'][name]
                
                c1, c2 = st.columns(2)
                chart_data["Age/Birth"] = c1.text_input("Age / Birth Date", value=chart_data.get("Age/Birth", ""), key=f"age_{name}")
                chart_data["Appearance"] = c2.text_input("Physical Appearance", value=chart_data.get("Appearance", ""), key=f"app_{name}")
                
                chart_data["Backstory"] = st.text_area("History / Backstory", value=chart_data.get("Backstory", ""), height=150, key=f"back_{name}")
                chart_data["Personality"] = st.text_area("Personality Traits", value=chart_data.get("Personality", ""), height=100, key=f"pers_{name}")
                chart_data["Arc"] = st.text_area("Character Arc (How they change)", value=chart_data.get("Arc", ""), height=200, key=f"arc_{name}")

# Step 8: The Scene List (PBI-S.15)
elif step == "8. The Scene List":
    st.header("Step 8: The Scene List")
    st.markdown("""
    Break your four-page summary into a list of scenes. 
    Each scene should have a clear POV character and a specific purpose.
    """)

    # Get labels and Step 6 content for context
    sections = ["Setup", "Disaster 1", "Disaster 2", "Disaster 3", "Resolution"]
    step6_pages = novel_data.get('step6_pages', [""] * 5)
    
    # Get character names for POV selection
    char_names = [c['Name'] for c in novel_data.get('characters', []) if c.get('Name')]
    if not char_names:
        char_names = ["Protagonist"]

    # Migration & Initialization
    if 'scene_list' not in novel_data:
        novel_data['scene_list'] = []
    
    for scene in novel_data['scene_list']:
        if 'Section' not in scene:
            scene['Section'] = "Setup"
        if 'id' not in scene:
            # Generate a stable ID based on existing info if possible, or new uuid
            scene['id'] = str(uuid.uuid4())

    # Initialize scene list if empty
    if not novel_data['scene_list']:
        novel_data['scene_list'] = [
            {"id": str(uuid.uuid4()), "POV Character": char_names[0], "Description": "Opening scene...", "Location": "TBD", "Section": "Setup"}
        ]

    # Display sections as expanders
    for i, section_label in enumerate(sections):
        with st.expander(f"📂 Section {i+1}: {section_label}", expanded=(i == 0)):
            # Context from Step 6
            st.caption("Reference (Step 6 Expansion):")
            st.info(step6_pages[i] if step6_pages[i] else "*(No content from Step 6)*")
            
            # Get scenes for this section in their current list order
            section_scenes = [s for s in novel_data['scene_list'] if s.get('Section') == section_label]
            
            for j, scene in enumerate(section_scenes):
                # Find current global index
                global_idx = novel_data['scene_list'].index(scene)
                
                with st.container(border=True):
                    c1, c2, c3 = st.columns([2, 2, 1.5])
                    
                    with c1:
                        scene['POV Character'] = st.selectbox(
                            f"POV Character", 
                            options=char_names, 
                            index=char_names.index(scene['POV Character']) if scene['POV Character'] in char_names else 0,
                            key=f"scene_pov_{scene['id']}"
                        )
                    with c2:
                        scene['Location'] = st.text_input(
                            f"Location", 
                            value=scene.get('Location', ""), 
                            key=f"scene_loc_{scene['id']}"
                        )
                    with c3:
                        st.write("") # Spacer
                        col_up, col_down, col_move, col_del = st.columns([1, 1, 2, 1])
                        with col_up:
                            if st.button("⬆️", key=f"up_{scene['id']}") and global_idx > 0:
                                novel_data['scene_list'].insert(global_idx - 1, novel_data['scene_list'].pop(global_idx))
                                st.rerun()
                        with col_down:
                            if st.button("⬇️", key=f"down_{scene['id']}") and global_idx < len(novel_data['scene_list']) - 1:
                                novel_data['scene_list'].insert(global_idx + 1, novel_data['scene_list'].pop(global_idx))
                                st.rerun()
                        with col_del:
                            if st.button("🗑️", key=f"del_{scene['id']}"):
                                novel_data['scene_list'].pop(global_idx)
                                st.rerun()
                        with col_move:
                            target_section = st.selectbox(
                                "Move", 
                                options=sections, 
                                index=sections.index(section_label),
                                key=f"move_{scene['id']}",
                                label_visibility="collapsed"
                            )
                            if target_section != section_label:
                                scene['Section'] = target_section
                                st.rerun()

                    scene['Description'] = st.text_area(
                        "What happens in this scene?", 
                        value=scene.get('Description', ""), 
                        key=f"scene_desc_{scene['id']}",
                        height=100
                    )

            if st.button(f"➕ Add Scene to {section_label}", key=f"add_to_{section_label}"):
                novel_data['scene_list'].append(
                    {"id": str(uuid.uuid4()), "POV Character": char_names[0], "Description": "", "Location": "TBD", "Section": section_label}
                )
                st.rerun()

    st.info("💡 Pro-tip: Reorder scenes using the arrows to refine the narrative flow within and between sections.")

# Step 9: The Narrative Outline
elif step == "9. The Narrative Outline":
    st.header("Step 9: The Narrative Outline")
    st.markdown("""
    Expand each scene from your **Step 8 Scene List** into a detailed narrative outline. 
    Scenes are organized by their narrative section for clarity.
    """)

    all_scenes = novel_data.get('scene_list', [])
    sections = ["Setup", "Disaster 1", "Disaster 2", "Disaster 3", "Resolution"]
    
    if not all_scenes or (len(all_scenes) == 1 and not all_scenes[0]['Description']):
         st.warning("⚠️ No scenes found. Please go to **Step 8: The Scene List** to define your scenes first.")
    else:
        if 'scene_outlines' not in novel_data:
            novel_data['scene_outlines'] = {}

        # Sort scenes by section to match Step 8 visual flow
        scene_counter = 1
        for section in sections:
            section_scenes = [s for s in all_scenes if s.get('Section') == section]
            if section_scenes:
                st.subheader(f"📂 {section}")
                for scene in section_scenes:
                    pov = scene.get('POV Character', 'Unknown')
                    desc = scene.get('Description', 'No description')
                    loc = scene.get('Location', 'TBD')
                    scene_id = scene.get('id')
                    
                    with st.expander(f"🎬 Scene {scene_counter}: {desc[:50]}...", expanded=True):
                        st.caption(f"POV: {pov} | Location: {loc}")
                        st.write(f"**Brief:** {desc}")
                        
                        current_outline = novel_data['scene_outlines'].get(scene_id, "")
                        new_outline = st.text_area(
                            f"Detailed Outline for Scene {scene_counter}",
                            value=current_outline,
                            height=200,
                            key=f"outline_{scene_id}",
                            label_visibility="collapsed"
                        )
                        novel_data['scene_outlines'][scene_id] = new_outline
                        scene_counter += 1

# Step 10: The First Draft
elif step == "10. The First Draft":
    st.header("Step 10: The First Draft")
    st.markdown("""
    It's time to write! Select a scene from your outline and start drafting. 
    Your planning from previous steps is available as a reference.
    """)

    all_scenes = novel_data.get('scene_list', [])
    sections = ["Setup", "Disaster 1", "Disaster 2", "Disaster 3", "Resolution"]
    
    # Create sorted list for selection
    sorted_scenes = []
    for section in sections:
        sorted_scenes.extend([s for s in all_scenes if s.get('Section') == section])

    if not sorted_scenes or (len(sorted_scenes) == 1 and not sorted_scenes[0]['Description']):
        st.warning("⚠️ No scenes found. Please complete the previous steps first.")
    else:
        if 'scene_content' not in novel_data:
            novel_data['scene_content'] = {}

        # Scene selection
        scene_options = [f"Scene {i+1} ({s.get('Section')}): {s['Description'][:30]}..." for i, s in enumerate(sorted_scenes)]
        selected_scene_idx = st.selectbox("Select a scene to write:", range(len(scene_options)), format_func=lambda x: scene_options[x])
        
        selected_scene = sorted_scenes[selected_scene_idx]
        scene_id = selected_scene.get('id')
        pov = selected_scene.get('POV Character', 'Unknown')
        desc = selected_scene.get('Description', '')
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📜 Reference")
            st.write(f"**POV:** {pov}")
            st.write(f"**Brief:** {desc}")
            
            with st.expander("📝 Scene Outline (Step 9)", expanded=True):
                outline = novel_data.get('scene_outlines', {}).get(scene_id, "*(No outline found)*")
                st.write(outline)
            
            with st.expander("👤 Character traits", expanded=False):
                charts = novel_data.get('character_charts', {}).get(pov, {})
                if charts:
                    st.write(f"**Appearance:** {charts.get('Appearance', 'N/A')}")
                    st.write(f"**Backstory:** {charts.get('Backstory', 'N/A')}")
                    st.write(f"**Arc:** {charts.get('Arc', 'N/A')}")
                else:
                    st.write("No character chart found for this POV.")

        with col2:
            st.subheader(f"✍️ Writing: Scene {selected_scene_idx + 1}")
            
            current_prose = novel_data['scene_content'].get(scene_id, "")
            new_prose = st.text_area(
                "Write your prose here:",
                value=current_prose,
                height=600,
                key=f"prose_{scene_id}",
                label_visibility="collapsed"
            )
            novel_data['scene_content'][scene_id] = new_prose
            
            word_count = len(new_prose.split()) if new_prose else 0
            st.caption(f"Word count for this scene: {word_count}")

# Placeholder for other steps
else:
    st.header(step)
    st.write("This section is currently under construction for the Proof of Concept.")

# PBI-S.5: Snapshot & Import
st.sidebar.divider()

# Export
# Now we export ALL novels in a bundle
export_data = {
    "version": "2.0",
    "active_novel": st.session_state.current_novel,
    "novels": st.session_state.novels
}
json_data = json.dumps(export_data, indent=2)
st.sidebar.download_button(
    label="💾 Download All Novels (JSON)",
    data=json_data,
    file_name="snowflake_archive.json",
    mime="application/json"
)

# Import
uploaded_file = st.sidebar.file_uploader("📂 Import Archive/Draft (JSON)", type="json")
if uploaded_file is not None:
    try:
        imported_data = json.load(uploaded_file)
        
        # Check if it's a new multi-novel archive (v2.0)
        if isinstance(imported_data, dict) and imported_data.get("version") == "2.0":
            st.session_state.novels = imported_data["novels"]
            st.session_state.current_novel = imported_data["active_novel"]
            # Save all imported novels to DB
            for name, data in st.session_state.novels.items():
                db.save_novel(name, data)
            st.sidebar.success("✅ Archive imported and saved to DB!")
            st.rerun()
            
        # Or if it's an old single-novel draft
        elif isinstance(imported_data, dict) and 'step1_hook' in imported_data:
            # Add it as a new novel
            import_name = f"Imported_{uuid.uuid4().hex[:4]}"
            new_data = create_empty_novel()
            new_data.update(imported_data)
            st.session_state.novels[import_name] = new_data
            db.save_novel(import_name, new_data) # Persist to DB
            st.session_state.current_novel = import_name
            st.sidebar.success(f"✅ Draft imported as '{import_name}' and saved to DB")
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid JSON format.")
    except Exception as e:
        st.sidebar.error(f"❌ Error loading JSON: {e}")

# --- Auto-save current state to DB ---
if 'current_novel' in st.session_state and 'novels' in st.session_state:
    current_name = st.session_state.current_novel
    if current_name in st.session_state.novels:
        db.save_novel(current_name, st.session_state.novels[current_name])
