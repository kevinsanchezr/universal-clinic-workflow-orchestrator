import { ClinicRecord, DashboardData, LaunchWorkflowRequest, LaunchWorkflowResponse, RunDetail } from "@/types";

function getApiBase() {
  if (typeof window === "undefined") {
    return process.env.API_INTERNAL_BASE_URL ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://backend:8000/api";
  }
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
}

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${getApiBase()}${path}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`API request failed: ${path}`);
  }
  return response.json();
}

async function postJson<T>(path: string, body?: unknown): Promise<T> {
  const response = await fetch(`${getApiBase()}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!response.ok) {
    throw new Error(`API request failed: ${path}`);
  }
  return response.json();
}

export const api = {
  clinics: () => getJson<ClinicRecord[]>("/clinics"),
  dashboard: () => getJson<DashboardData>("/dashboard"),
  runs: () => getJson<Array<Record<string, unknown>>>("/runs"),
  run: (id: string) => getJson<RunDetail>(`/runs/${id}`),
  handoffs: () => getJson<Array<Record<string, unknown>>>("/handoffs"),
  simulators: () => getJson<Array<Record<string, unknown>>>("/simulators"),
  settings: () => getJson<Record<string, unknown>>("/settings"),
  templates: () => getJson<Array<Record<string, unknown>>>("/templates"),
  seed: () => postJson<{ status: string; seeded: boolean; reason?: string }>("/seed"),
  launchWorkflow: (body: LaunchWorkflowRequest) => postJson<LaunchWorkflowResponse>("/runs", body),
};
