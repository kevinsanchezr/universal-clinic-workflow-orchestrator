"use client";

import { create } from "zustand";

type UIState = {
  selectedRunId: string | null;
  setSelectedRunId: (runId: string | null) => void;
};

export const useUIStore = create<UIState>((set) => ({
  selectedRunId: null,
  setSelectedRunId: (selectedRunId) => set({ selectedRunId }),
}));
