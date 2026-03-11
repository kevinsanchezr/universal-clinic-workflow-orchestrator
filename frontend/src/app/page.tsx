import { api } from "@/lib/api";
import { MetricCard, Panel, StatusPill } from "@/components/ui";
import { RunTable } from "@/components/run-table";


export default async function DashboardPage() {
  const data = await api.dashboard();

  return (
    <div className="space-y-6">
      <section className="flex flex-col gap-3">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-accent">Operational Reliability Layer</p>
        <h1 className="text-4xl font-semibold tracking-tight">Clinic workflow execution with traceability-first controls</h1>
        <p className="max-w-3xl text-muted">
          Deterministic workflow orchestration across modern and legacy EHR surfaces with redacted audit trails, retry categorization,
          and structured human fallback.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Total workflow runs" value={data.metrics.total_runs ?? 0} />
        <MetricCard label="Active runs" value={data.metrics.active_runs ?? 0} />
        <MetricCard label="Open handoffs" value={data.metrics.open_handoffs ?? 0} tone="warning" />
        <MetricCard label="Completed" value={data.metrics.completed_today ?? 0} />
      </section>

      <section className="grid gap-6 xl:grid-cols-[2fr_1fr]">
        <Panel eyebrow="Live Runs" title="Execution feed">
          <RunTable runs={data.active_runs} />
        </Panel>
        <Panel eyebrow="Failure Signals" title="Categorized outcomes">
          <div className="space-y-3">
            {data.failures_by_reason.length === 0 && <p className="text-sm text-muted">No escalations or hard failures yet.</p>}
            {data.failures_by_reason.map((item) => (
              <div key={item.reason} className="flex items-center justify-between rounded-2xl border border-line p-4">
                <div>
                  <p className="font-medium capitalize">{item.reason}</p>
                  <p className="text-sm text-muted">Retry and escalation taxonomy bucket</p>
                </div>
                <StatusPill label={`${item.count}`} tone={item.reason === "failed" ? "danger" : "warning"} />
              </div>
            ))}
          </div>
        </Panel>
      </section>

      <section className="grid gap-6 xl:grid-cols-3">
        <Panel eyebrow="Handoff Queue" title="Needs human review">
          <div className="space-y-3">
            {data.handoff_queue.map((item) => (
              <div key={item.id} className="rounded-2xl border border-line p-4">
                <div className="flex items-center justify-between">
                  <StatusPill label={item.priority} tone="warning" />
                  <span className="font-mono text-xs text-muted">{new Date(item.created_at).toLocaleString()}</span>
                </div>
                <p className="mt-3 text-sm">{item.reason}</p>
              </div>
            ))}
          </div>
        </Panel>
        <Panel eyebrow="Workflow Library" title="Template coverage">
          <div className="space-y-3">
            {data.workflows.map((workflow) => (
              <div key={workflow.slug} className="rounded-2xl border border-line p-4">
                <p className="font-medium">{workflow.name}</p>
                <p className="font-mono text-xs text-muted">{workflow.slug}</p>
              </div>
            ))}
          </div>
        </Panel>
        <Panel eyebrow="Simulator Matrix" title="EHR surfaces">
          <div className="space-y-3">
            {data.simulators.map((sim) => (
              <div key={`${sim.clinic_name}-${sim.ehr_style}`} className="rounded-2xl border border-line p-4">
                <p className="font-medium">{sim.clinic_name}</p>
                <p className="text-sm text-muted">Adapter style: {sim.ehr_style}</p>
              </div>
            ))}
          </div>
        </Panel>
      </section>
    </div>
  );
}
