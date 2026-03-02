import { create } from 'zustand'

interface ProjectState {
  currentProjectId: number | null
  setCurrentProjectId: (id: number | null) => void
}

export const useProjectStore = create<ProjectState>((set) => ({
  currentProjectId: null,
  setCurrentProjectId: (id) => set({ currentProjectId: id }),
}))
