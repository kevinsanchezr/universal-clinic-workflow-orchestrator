export type DashboardData = {
  metrics: Record<string, number>;
  active_runs: Array<{
    id: string;
    template_name: string;
    clinic_name: string;
    status: string;
    outcome: string | null;
    confidence: number;
    current_step: string | null;
    created_at: string;
  }>;
  failures_by_reason: Array<{ reason: string; count: number }>;
  handoff_queue: Array<{
    id: string;
    status: string;
    priority: string;
    reason: string;
    created_at: string;
  }>;
  workflows: Array<{ name: string; slug: string; version: string }>;
  simulators: Array<{ clinic_name: string; ehr_style: string }>;
};

export type RunDetail = {
  id: string;
  status: string;
  outcome: string | null;
  confidence: number;
  ehr_style: string;
  current_step: string | null;
  redacted_input: Record<string, unknown>;
  state_snapshot: Record<string, unknown>;
  steps: Array<{
    id: string;
    step_key: string;
    status: string;
    action_type: string;
    confidence: number;
    rationale: string;
    retry_count: number;
    input_summary: Record<string, unknown>;
    output_summary: Record<string, unknown>;
    adapter_trace: Record<string, unknown>;
    created_at: string;
  }>;
};
