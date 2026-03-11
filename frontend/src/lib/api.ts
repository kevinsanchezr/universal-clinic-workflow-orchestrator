import { DashboardData, RunDetail } from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`API request failed: ${path}`);
  }
  return response.json();
}

export const api = {
  dashboard: () => getJson<DashboardData>("/dashboard"),
  runs: () => getJson<Array<Record<string, unknown>>>("/runs"),
  run: (id: string) => getJson<RunDetail>(`/runs/${id}`),
  handoffs: () => getJson<Array<Record<string, unknown>>>("/handoffs"),
  simulators: () => getJson<Array<Record<string, unknown>>>("/simulators"),
  settings: () => getJson<Record<string, unknown>>("/settings"),
  templates: () => getJson<Array<Record<string, unknown>>>("/templates"),
};
