import streamlit as st
import pandas as pd
import json
import uuid
import db
import i18n

# Initialize Localization
i18n.init_i18n()
_ = i18n.get_text

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
st.sidebar.title(_("sidebar.title"))

# Language Selector
selected_lang = st.sidebar.selectbox(
    "🌍 Language / Langue",
    options=i18n.SUPPORTED_LANGS,
    index=i18n.SUPPORTED_LANGS.index(st.session_state.lang),
    format_func=lambda x: "English" if x == "en" else "Français"
)
if selected_lang != st.session_state.lang:
    i18n.change_lang(selected_lang)

# Project Manager
st.sidebar.divider()
st.sidebar.subheader(_("sidebar.nav_header"))

# Select Novel
novel_list = list(st.session_state.novels.keys())
current_idx = novel_list.index(st.session_state.current_novel) if st.session_state.current_novel in novel_list else 0
selected_novel = st.sidebar.selectbox(_("sidebar.active_novel"), novel_list, index=current_idx)

if selected_novel != st.session_state.current_novel:
    st.session_state.current_novel = selected_novel
    st.rerun()

# Add New Novel
with st.sidebar.expander(_("sidebar.new_novel")):
    new_novel_name = st.text_input(_("sidebar.novel_title"), key="new_novel_name")
    if st.button(_("sidebar.create")):
        if new_novel_name and new_novel_name not in st.session_state.novels:
            st.session_state.novels[new_novel_name] = create_empty_novel()
            db.save_novel(new_novel_name, st.session_state.novels[new_novel_name])
            st.session_state.current_novel = new_novel_name
            st.rerun()
        elif new_novel_name:
            st.error("Title already exists!")

# Delete Novel
if len(st.session_state.novels) > 1:
    if st.sidebar.button(_("sidebar.delete")):
        old_name = st.session_state.current_novel
        del st.session_state.novels[old_name]
        db.delete_novel(old_name)
        st.session_state.current_novel = list(st.session_state.novels.keys())[0]
        st.rerun()

st.sidebar.divider()

step_options = _("sidebar.steps")
step = st.sidebar.radio(
    "Go to Step:",
    step_options
)

# Home Page content
if step == step_options[0]: # Home
    st.header(_("home.welcome", novel_name=st.session_state.current_novel))
    st.markdown(_("home.intro"))
    st.markdown("""
    ### ❄️ What is the Snowflake Method?
    Instead of starting from page one and hoping for the best (the "Pantser" approach), the Snowflake Method is a "Plotter" strategy. You begin with a single sentence and systematically grow it into a full-length manuscript through ten structured steps.

    ### 🛠️ How to use this tool:
    1.  **Iterative Growth:** Each step builds upon the work you did in the previous one. 
    2.  **Character & Plot:** You'll alternate between developing your story's plot and deepening your characters.
    3.  **Flexibility:** Don't be afraid to go back to earlier steps! If you discover something new about a character in Step 5, update Step 1 to match.
    4.  **Automatic Persistence:** Your work is automatically saved to a local database (`snowflake.db`) on your machine as you type. 
    5.  **Backups & Archives:** Use the **Download All Novels** button in the sidebar to export your entire archive for safekeeping.

    ### 🚀 Getting Started:
    Select **"1. The One-Sentence Hook"** from the sidebar to begin your journey!
    """)

# Step 1: The One-Sentence Hook (PBI-S.2)
elif step == step_options[1]:
    st.header(_("step1.header"))
    st.info(_("step1.info"))

    # Input
    hook = st.text_input(
        _("step1.label"),
        value=novel_data['step1_hook'],
        placeholder=_("step1.placeholder")
    )

    # Logic: Word count
    word_count = len(hook.split()) if hook else 0
    st.write(_("step1.word_count", count=word_count))

    # Validation
    if word_count > 15:
        st.warning(_("step1.warning"))
    elif 0 < word_count <= 15:
        st.success(_("step1.success"))

    # Save to state
    novel_data['step1_hook'] = hook

# Step 2: The One-Paragraph Summary (PBI-S.3)
elif step == step_options[2]:
    st.header(_("step2.header"))
    
    st.markdown(_("step2.markdown"))

    with st.expander(_("step2.expander_label"), expanded=True):
        st.info(_("step2.expander_info"))

    # Input
    summary = st.text_area(
        _("step2.label"),
        value=novel_data['step2_summary'],
        height=200,
        placeholder=_("step2.placeholder")
    )

    # Logic: Sentence count (approximate)
    sentence_count = len([s for s in summary.split('.') if s.strip()]) if summary else 0
    st.write(_("step2.sentence_count", count=sentence_count))

    # Validation
    if sentence_count == 5:
        st.success(_("step2.success"))
    elif sentence_count > 5:
        st.warning(_("step2.warning"))
    elif 0 < sentence_count < 5:
        st.info(_("step2.info", count=sentence_count))

    # Save to state
    novel_data['step2_summary'] = summary

# Step 3: Character Dossiers (PBI-S.13)
elif step == step_options[3]:
    st.header(_("step3.header"))
    st.markdown(_("step3.markdown"))

    # Initialize list if empty
    if not novel_data['characters']:
        novel_data['characters'] = [
            {"Name": _("step3.default_name"), "Motivation": "", "Goal": "", "Conflict": "", "Epiphany": ""}
        ]

    # Display characters as cards
    for i, char in enumerate(novel_data['characters']):
        with st.container(border=True):
            col_header, col_delete = st.columns([5, 1])
            
            with col_header:
                # Update name directly in session state
                novel_data['characters'][i]['Name'] = st.text_input(
                    _("step3.char_name_placeholder"), 
                    value=char['Name'], 
                    key=f"char_name_{i}",
                    label_visibility="collapsed"
                )
            
            with col_delete:
                if st.button("🗑️", key=f"del_char_{i}", help=_("step3.delete_help")):
                    novel_data['characters'].pop(i)
                    st.rerun()

            c1, c2 = st.columns(2)
            with c1:
                novel_data['characters'][i]['Motivation'] = st.text_area(
                    _("step3.motivation_label"), 
                    value=char['Motivation'], 
                    key=f"char_mot_{i}", 
                    height=100
                )
                novel_data['characters'][i]['Goal'] = st.text_area(
                    _("step3.goal_label"), 
                    value=char['Goal'], 
                    key=f"char_goal_{i}", 
                    height=100
                )
            with c2:
                novel_data['characters'][i]['Conflict'] = st.text_area(
                    _("step3.conflict_label"), 
                    value=char['Conflict'], 
                    key=f"char_conf_{i}", 
                    height=100
                )
                novel_data['characters'][i]['Epiphany'] = st.text_area(
                    _("step3.epiphany_label"), 
                    value=char['Epiphany'], 
                    key=f"char_epi_{i}", 
                    height=100
                )

    if st.button(_("step3.add_character")):
        novel_data['characters'].append(
            {"Name": f"{_('sidebar.novel_title')} {len(novel_data['characters']) + 1}", "Motivation": "", "Goal": "", "Conflict": "", "Epiphany": ""}
        )
        st.rerun()

# Step 4: The One-Page Summary
elif step == step_options[4]:
    st.header(_("step4.header"))
    st.markdown(_("step4.markdown"))

    # Initialize step 4 data if not present
    if 'step4_paragraphs' not in novel_data:
        novel_data['step4_paragraphs'] = ["", "", "", "", ""]

    # Get Step 2 sentences to use as prompts
    step2_text = novel_data['step2_summary']
    sentences = [s.strip() + "." for s in step2_text.split('.') if s.strip()]
    
    # Ensure we have 5 prompts
    prompts = sentences + [_("step4.prompt_fallback")] * (5 - len(sentences))

    labels = _("step4.labels")
    
    updated_paragraphs = []
    for i in range(5):
        st.subheader(labels[i])
        st.caption(_("step4.prompt_caption", prompt=prompts[i]))
        para = st.text_area(
            _("step4.para_label", num=i+1),
            value=novel_data['step4_paragraphs'][i],
            height=150,
            key=f"para_{i}"
        )
        updated_paragraphs.append(para)

    novel_data['step4_paragraphs'] = updated_paragraphs

# Step 5: Character Synopses
elif step == step_options[5]:
    st.header(_("step5.header"))
    st.markdown(_("step5.markdown"))

    characters = novel_data.get('characters', [])
    
    if not characters or (len(characters) == 1 and characters[0]['Name'] == _("step3.default_name") and not characters[0]['Motivation']):
        st.warning(_("step5.no_chars_warning"))
    else:
        # Initialize synopses dictionary if not present
        if 'character_synopses' not in novel_data:
            novel_data['character_synopses'] = {}

        for char in characters:
            name = char.get('Name', 'Unnamed Character')
            if not name: continue
            
            with st.expander(_("step5.expander_label", name=name), expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write(_("step5.ref_header"))
                    st.write(_("step5.motivation", val=char.get('Motivation', 'N/A')))
                    st.write(_("step5.goal", val=char.get('Goal', 'N/A')))
                    st.write(_("step5.conflict", val=char.get('Conflict', 'N/A')))
                
                with col2:
                    current_synopsis = novel_data['character_synopses'].get(name, "")
                    new_synopsis = st.text_area(
                        _("step5.synopsis_label", name=name),
                        value=current_synopsis,
                        height=250,
                        key=f"synopsis_{name}",
                        label_visibility="collapsed"
                    )
                    novel_data['character_synopses'][name] = new_synopsis

# Step 6: The Four-Page Summary
elif step == step_options[6]:
    st.header(_("step6.header"))
    st.markdown(_("step6.markdown"))

    # Initialize step 6 data if not present
    if 'step6_pages' not in novel_data:
        novel_data['step6_pages'] = ["", "", "", "", ""]

    # Get Step 4 paragraphs to use as prompts
    step4_paras = novel_data.get('step4_paragraphs', ["", "", "", "", ""])
    
    labels = _("step6.labels")
    
    updated_pages = []
    for i in range(5):
        st.subheader(labels[i])
        with st.expander(_("step6.ref_expander"), expanded=False):
            st.write(step4_paras[i] if step4_paras[i] else _("step6.empty_ref"))
            
        page_text = st.text_area(
            _("step6.expansion_label", label=labels[i]),
            value=novel_data['step6_pages'][i],
            height=400,
            key=f"page_{i}",
            label_visibility="collapsed"
        )
        updated_pages.append(page_text)

    novel_data['step6_pages'] = updated_pages

# Step 7: Character Charts
elif step == step_options[7]:
    st.header(_("step7.header"))
    st.markdown(_("step7.markdown"))

    characters = novel_data.get('characters', [])
    
    if not characters or (len(characters) == 1 and characters[0]['Name'] == _("step3.default_name") and not characters[0]['Motivation']):
        st.warning(_("step5.no_chars_warning"))
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
            
            with st.expander(_("step7.expander_label", name=name), expanded=True):
                # References
                with st.container():
                    st.caption(_("step7.ref_caption"))
                    cols = st.columns(3)
                    cols[0].write(_("step7.goal", val=char.get('Goal', 'N/A')))
                    cols[1].write(_("step7.conflict", val=char.get('Conflict', 'N/A')))
                    cols[2].write(_("step7.epiphany", val=char.get('Epiphany', 'N/A')))

                chart_data = novel_data['character_charts'][name]
                
                c1, c2 = st.columns(2)
                chart_data["Age/Birth"] = c1.text_input(_("step7.age_label"), value=chart_data.get("Age/Birth", ""), key=f"age_{name}")
                chart_data["Appearance"] = c2.text_input(_("step7.appearance_label"), value=chart_data.get("Appearance", ""), key=f"app_{name}")
                
                chart_data["Backstory"] = st.text_area(_("step7.backstory_label"), value=chart_data.get("Backstory", ""), height=150, key=f"back_{name}")
                chart_data["Personality"] = st.text_area(_("step7.personality_label"), value=chart_data.get("Personality", ""), height=100, key=f"pers_{name}")
                chart_data["Arc"] = st.text_area(_("step7.arc_label"), value=chart_data.get("Arc", ""), height=200, key=f"arc_{name}")

# Step 8: The Scene List (PBI-S.15)
elif step == step_options[8]:
    st.header(_("step8.header"))
    st.markdown(_("step8.markdown"))

    # Get labels and Step 6 content for context
    sections = _("step8.sections")
    step6_pages = novel_data.get('step6_pages', [""] * 5)
    
    # Get character names for POV selection
    char_names = [c['Name'] for c in novel_data.get('characters', []) if c.get('Name')]
    if not char_names:
        char_names = [_("step8.default_pov")]

    # Migration & Initialization
    if 'scene_list' not in novel_data:
        novel_data['scene_list'] = []
    
    for scene in novel_data['scene_list']:
        if 'Section' not in scene:
            scene['Section'] = sections[0]
        if 'id' not in scene:
            # Generate a stable ID based on existing info if possible, or new uuid
            scene['id'] = str(uuid.uuid4())

    # Initialize scene list if empty
    if not novel_data['scene_list']:
        novel_data['scene_list'] = [
            {"id": str(uuid.uuid4()), "POV Character": char_names[0], "Description": "Opening scene...", "Location": "TBD", "Section": sections[0]}
        ]

    # Display sections as expanders
    for i, section_label in enumerate(sections):
        with st.expander(_("step8.section_expander", num=i+1, label=section_label), expanded=(i == 0)):
            # Context from Step 6
            st.caption(_("step8.ref_caption"))
            st.info(step6_pages[i] if step6_pages[i] else _("step8.empty_ref"))
            
            # Get scenes for this section in their current list order
            # Note: We must be careful with comparison if Section names are translated in DB.
            # Best practice is to keep internal Section keys English or use order_index.
            # For now, let's assume we map indices if possible.
            section_scenes = [s for s in novel_data['scene_list'] if s.get('Section') == section_label or s.get('Section') == ["Setup", "Disaster 1", "Disaster 2", "Disaster 3", "Resolution"][i]]
            
            for j, scene in enumerate(section_scenes):
                # Find current global index
                global_idx = novel_data['scene_list'].index(scene)
                
                with st.container(border=True):
                    c1, c2, c3 = st.columns([2, 2, 1.5])
                    
                    with c1:
                        scene['POV Character'] = st.selectbox(
                            _("step8.pov_label"), 
                            options=char_names, 
                            index=char_names.index(scene['POV Character']) if scene['POV Character'] in char_names else 0,
                            key=f"scene_pov_{scene['id']}"
                        )
                    with c2:
                        scene['Location'] = st.text_input(
                            _("step8.loc_label"), 
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
                                _("step8.move_label"), 
                                options=sections, 
                                index=sections.index(section_label) if section_label in sections else 0,
                                key=f"move_{scene['id']}",
                                label_visibility="collapsed"
                            )
                            if target_section != section_label:
                                scene['Section'] = target_section
                                st.rerun()

                    scene['Description'] = st.text_area(
                        _("step8.desc_label"), 
                        value=scene.get('Description', ""), 
                        key=f"scene_desc_{scene['id']}",
                        height=100
                    )

            if st.button(_("step8.add_scene", label=section_label), key=f"add_to_{section_label}"):
                novel_data['scene_list'].append(
                    {"id": str(uuid.uuid4()), "POV Character": char_names[0], "Description": "", "Location": "TBD", "Section": section_label}
                )
                st.rerun()

    st.info(_("step8.tip"))

# Step 9: The Narrative Outline
elif step == step_options[9]:
    st.header(_("step9.header"))
    st.markdown(_("step9.markdown"))

    all_scenes = novel_data.get('scene_list', [])
    sections = _("step8.sections")
    
    if not all_scenes or (len(all_scenes) == 1 and not all_scenes[0]['Description']):
         st.warning(_("step9.no_scenes_warning"))
    else:
        if 'scene_outlines' not in novel_data:
            novel_data['scene_outlines'] = {}

        # Sort scenes by section to match Step 8 visual flow
        scene_counter = 1
        for section_label in sections:
            # Note: We must handle the mapping carefully as in Step 8
            orig_sections = ["Setup", "Disaster 1", "Disaster 2", "Disaster 3", "Resolution"]
            orig_label = orig_sections[sections.index(section_label)]
            section_scenes = [s for s in all_scenes if s.get('Section') == section_label or s.get('Section') == orig_label]
            
            if section_scenes:
                st.subheader(f"📂 {section_label}")
                for scene in section_scenes:
                    pov = scene.get('POV Character', 'Unknown')
                    desc = scene.get('Description', 'No description')
                    loc = scene.get('Location', 'TBD')
                    scene_id = scene.get('id')
                    
                    with st.expander(_("step9.scene_expander", num=scene_counter, desc=desc[:50]), expanded=True):
                        st.caption(_("step9.ref_caption", pov=pov, loc=loc))
                        st.write(_("step9.brief_label", desc=desc))
                        
                        current_outline = novel_data['scene_outlines'].get(scene_id, "")
                        new_outline = st.text_area(
                            _("step9.outline_label", num=scene_counter),
                            value=current_outline,
                            height=200,
                            key=f"outline_{scene_id}",
                            label_visibility="collapsed"
                        )
                        novel_data['scene_outlines'][scene_id] = new_outline
                        scene_counter += 1

# Step 10: The First Draft
elif step == step_options[10]:
    st.header(_("step10.header"))
    st.markdown(_("step10.markdown"))

    all_scenes = novel_data.get('scene_list', [])
    sections = _("step8.sections")
    
    # Create sorted list for selection
    sorted_scenes = []
    for section_label in sections:
        # Note: We must handle the mapping carefully as in Step 8/9
        orig_sections = ["Setup", "Disaster 1", "Disaster 2", "Disaster 3", "Resolution"]
        orig_label = orig_sections[sections.index(section_label)]
        sorted_scenes.extend([s for s in all_scenes if s.get('Section') == section_label or s.get('Section') == orig_label])

    if not sorted_scenes or (len(sorted_scenes) == 1 and not sorted_scenes[0]['Description']):
        st.warning(_("step10.no_scenes_warning"))
    else:
        if 'scene_content' not in novel_data:
            novel_data['scene_content'] = {}

        # Scene selection
        scene_options = [_("step10.option_label", num=i+1, section=s.get('Section'), desc=s['Description'][:30]) for i, s in enumerate(sorted_scenes)]
        selected_scene_idx = st.selectbox(_("step10.select_label"), range(len(scene_options)), format_func=lambda x: scene_options[x])
        
        selected_scene = sorted_scenes[selected_scene_idx]
        scene_id = selected_scene.get('id')
        pov = selected_scene.get('POV Character', 'Unknown')
        desc = selected_scene.get('Description', '')
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader(_("step10.ref_header"))
            st.write(_("step10.pov_label", val=pov))
            st.write(_("step10.brief_label", val=desc))
            
            with st.expander(_("step10.outline_expander"), expanded=True):
                outline = novel_data.get('scene_outlines', {}).get(scene_id, _("step10.empty_outline"))
                st.write(outline)
            
            with st.expander(_("step10.traits_expander"), expanded=False):
                charts = novel_data.get('character_charts', {}).get(pov, {})
                if charts:
                    st.write(_("step10.appearance", val=charts.get('Appearance', 'N/A')))
                    st.write(_("step10.backstory", val=charts.get('Backstory', 'N/A')))
                    st.write(_("step10.arc", val=charts.get('Arc', 'N/A')))
                else:
                    st.write(_("step10.no_traits"))

        with col2:
            st.subheader(_("step10.writing_header", num=selected_scene_idx + 1))
            
            current_prose = novel_data['scene_content'].get(scene_id, "")
            new_prose = st.text_area(
                _("step10.prose_placeholder"),
                value=current_prose,
                height=600,
                key=f"prose_{scene_id}",
                label_visibility="collapsed"
            )
            novel_data['scene_content'][scene_id] = new_prose
            
            word_count = len(new_prose.split()) if new_prose else 0
            st.caption(_("step10.word_count", count=word_count))

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
    label=_("export_import.download_label"),
    data=json_data,
    file_name="snowflake_archive.json",
    mime="application/json"
)

# Import
uploaded_file = st.sidebar.file_uploader(_("export_import.import_label"), type="json")
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
            st.sidebar.success(_("export_import.import_success_archive"))
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
            st.sidebar.success(_("export_import.import_success_draft", name=import_name))
            st.rerun()
        else:
            st.sidebar.error(_("export_import.import_error_format"))
    except Exception as e:
        st.sidebar.error(_("export_import.import_error_load", error=e))

# --- Auto-save current state to DB ---
if 'current_novel' in st.session_state and 'novels' in st.session_state:
    current_name = st.session_state.current_novel
    if current_name in st.session_state.novels:
        db.save_novel(current_name, st.session_state.novels[current_name])
