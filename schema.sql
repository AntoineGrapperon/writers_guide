-- "The Architect's Ledger" - Database Schema

-- Users & Projects
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    one_sentence_summary VARCHAR(255), -- The "Hook" (Step 1)
    one_paragraph_summary TEXT, -- Step 2 (5 sentences)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- The "Sprout" (Step 3: Characters)
CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    motivation TEXT, -- Abstract Want
    goal TEXT, -- Concrete Want
    conflict TEXT, -- Preventing Goal
    epiphany TEXT, -- Lesson Learned
    one_sentence_storyline TEXT, -- Character's specific arc summary
    one_paragraph_summary TEXT, -- Expanded arc summary
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- The "Sprout" (Threads/Subplots)
-- Events are organized into Threads (e.g., "A-Plot", "Romance Arc")
CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL, -- e.g., "Main Plot", "Mystery Subplot"
    description TEXT,
    color_code VARCHAR(7) DEFAULT '#CCCCCC' -- For UI visualization
);

-- The "Roots" (Timeline of Events)
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    thread_id INTEGER REFERENCES threads(id) ON DELETE SET NULL, -- An event belongs to a thread
    summary TEXT NOT NULL, -- Short description of what happens
    order_index INTEGER NOT NULL, -- Chronological order
    estimated_duration VARCHAR(50), -- e.g., "2 hours", "3 days" (Text for flexibility or Interval for precision)
    notes TEXT, -- Expanded description
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Linking Characters to Events (Many-to-Many)
-- Tracks who is present in which event
CREATE TABLE event_characters (
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    character_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
    is_pov BOOLEAN DEFAULT FALSE, -- Is this character the Point of View for this event?
    PRIMARY KEY (event_id, character_id)
);

-- The "Trunk" (Chapters)
CREATE TABLE chapters (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(255),
    chapter_number INTEGER NOT NULL,
    summary TEXT,
    target_word_count INTEGER DEFAULT 3000, -- Default goal
    actual_word_count INTEGER DEFAULT 0, -- Measured progress
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Linking Events to Chapters
-- An event usually falls into one chapter, but could span multiple?
-- Assumption: Events are atomic units within chapters.
CREATE TABLE chapter_events (
    chapter_id INTEGER REFERENCES chapters(id) ON DELETE CASCADE,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    order_index INTEGER NOT NULL, -- Order within the chapter
    PRIMARY KEY (chapter_id, event_id)
);

-- The "Canopy" (Scenes - Detailed expansion of Events)
-- Sometimes 1 Event = 1 Scene, but sometimes 1 Event = Multiple Scenes.
-- For MVP, let's treat "Scene" as the writing unit linked to a Chapter.
CREATE TABLE scenes (
    id SERIAL PRIMARY KEY,
    chapter_id INTEGER REFERENCES chapters(id) ON DELETE CASCADE,
    pov_character_id INTEGER REFERENCES characters(id) ON DELETE SET NULL,
    title VARCHAR(255),
    content TEXT, -- The actual prose draft
    order_index INTEGER NOT NULL,
    status VARCHAR(50) DEFAULT 'draft', -- 'draft', 'revised', 'polished'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
