# Product Backlog: "The Architect's Ledger" MVP

## Epic 1: Foundation & Data Architecture
**Goal:** Establish the core data models and API structure to support the relational complexity of the Snowflake method.
- [ ] **PBI-1.1: Database Schema Design**
    - Design PostgreSQL schema for `Projects`, `Characters`, `Threads` (subplots), `Events`, `Scenes`, and `Chapters`.
    - define relationships: Events belong to Threads; Scenes link to Characters (POV) and Chapters.
    - *Deliverable:* valid `.sql` schema file.
- [ ] **PBI-1.2: Project Initialization (Backend)**
    - Set up Node.js/Express (TS) project structure.
    - Configure TypeORM/Prisma for database interaction.
    - *Deliverable:* compiling backend with health check API.
- [ ] **PBI-1.3: Project Initialization (Frontend)**
    - Set up React (Vite + TS) project.
    - Configure routing (TanStack Router) and state management (Zustand/Context).
    - *Deliverable:* running frontend shell.

## Epic 2: The "Seed" & "Sprout" (Steps 1-2)
**Goal:** Enable users to define the high-level concept and initial character/thread metadata.
- [ ] **PBI-2.1: Project Creation & "The Hook"**
    - UI: Form for Project Title, 15-word Hook, and 5-sentence Summary.
    - Logic: Word count validation for the Hook.
    - *Deliverable:* Functional "New Project" flow.
- [ ] **PBI-2.2: Character & Thread Management**
    - UI: "Dossier" view to CRUD Characters (Name, Motivation, Goal, Conflict).
    - UI: "Threads" view to define subplots (e.g., "A-Plot", "Romantic Subplot").
    - *Deliverable:* Managing the entities that will populate the grid.

## Epic 3: The "Roots" (Timeline & Grid)
**Goal:** Build the core spreadsheet-like interface for plotting events across threads.
- [ ] **PBI-3.1: The Event Grid (UI)**
    - UI: Implement TanStack Table for the "Roots" view.
    - Columns: Event Summary, Timeline/Date, Estimated Duration.
    - *Deliverable:* Interactive table.
- [ ] **PBI-3.2: Thread Assignment Logic**
    - Feature: Assign Events to specific Threads and Characters.
    - Visual: Color-code rows/cells based on the assigned Thread.
    - *Deliverable:* Visual distinction between plot lines.
- [ ] **PBI-3.3: Drag-and-Drop Reordering**
    - Feature: Reorder events in the grid to adjust the chronology.
    - Logic: Update `order_index` in DB.
    - *Deliverable:* Smooth drag-and-drop experience.

## Epic 4: The "Trunk" & "Canopy" (Structure & Analytics)
**Goal:** Group events into chapters and visualize progress.
- [ ] **PBI-4.1: Chapter Management**
    - UI: Interface to create Chapters and assign Scenes/Events to them.
    - Logic: Calculate estimated word count per chapter based on scenes.
    - *Deliverable:* Chapter outline view.
- [ ] **PBI-4.2: The "Presence Matrix"**
    - Visualization: A heatmap/grid showing which Characters appear in which Chapters.
    - *Deliverable:* Auto-generated visual report.
- [ ] **PBI-4.3: Progress Analytics**
    - Dashboard: Charts for "Planned vs Actual" word counts (using Recharts).
    - *Deliverable:* The "Engineer's Dashboard" view.

## Epic 5: The "Snowflake" Workflow
**Goal:** Connect the steps and enforce the "cycling back" methodology.
- [ ] **PBI-5.1: The Navigation Sidebar**
    - UI: Persistent sidebar tracking the 10 Snowflake steps.
    - Logic: Lock/Unlock steps based on completion (optional strict mode).
    - *Deliverable:* Guided navigation.
- [ ] **PBI-5.2: The "Re-Sprout" Consistency Check**
    - Feature: When a Character name/trait changes, flag related Scenes as "Needs Review."
    - *Deliverable:* Notification system for consistency.
