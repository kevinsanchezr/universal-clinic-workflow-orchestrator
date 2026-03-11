import { api } from "@/lib/api";
import { MetricCard, Panel, StatusPill } from "@/components/ui";
import { RunTable } from "@/components/run-table";


export default async function DashboardPage() {
  const data = await api.dashboard();
  const demo = data.demo_spotlight;

  return (
    <div className="space-y-6">
      <section className="flex flex-col gap-3">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-accent">Operational Reliability Layer for AI Employees in Clinics</p>
        <h1 className="text-4xl font-semibold tracking-tight">The missing infrastructure that makes clinic AI actually deployable</h1>
        <p className="max-w-3xl text-muted">
          Reliable execution across legacy and modern EHR surfaces, with confidence scoring, human fallback, redacted audit trails,
          and visible business outcomes.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Total workflow runs" value={data.metrics.total_runs ?? 0} />
        <MetricCard label="Active runs" value={data.metrics.active_runs ?? 0} />
        <MetricCard label="Open handoffs" value={data.metrics.open_handoffs ?? 0} tone="warning" />
        <MetricCard label="Completed" value={data.metrics.completed_today ?? 0} />
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Panel eyebrow="Primary Demo" title={demo.headline}>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <MetricCard label="Revenue recovered" value={`$${demo.expected_revenue_recovered}`} />
            <MetricCard label="Staff time saved" value={`${demo.manual_staff_minutes_saved} min`} />
            <MetricCard label="Confidence" value={demo.confidence.toFixed(2)} />
            <MetricCard label="PHI in logs" value={demo.phi_persisted_in_logs} />
          </div>
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            <div className="rounded-2xl border border-line p-4">
              <p className="text-sm text-muted">Step 1</p>
              <p className="mt-2 font-medium">Cancellation identified</p>
              <StatusPill label={demo.cancellation_identified ? "complete" : "pending"} tone={demo.cancellation_identified ? "success" : "neutral"} />
            </div>
            <div className="rounded-2xl border border-line p-4">
              <p className="text-sm text-muted">Step 2</p>
              <p className="mt-2 font-medium">Best-fit patient selected</p>
              <StatusPill label={demo.best_fit_patient_selected ? "complete" : "pending"} tone={demo.best_fit_patient_selected ? "success" : "neutral"} />
            </div>
            <div className="rounded-2xl border border-line p-4">
              <p className="text-sm text-muted">Step 3</p>
              <p className="mt-2 font-medium">Slot refilled in LegacyEHR</p>
              <StatusPill label={demo.slot_refilled ? "complete" : "pending"} tone={demo.slot_refilled ? "success" : "neutral"} />
            </div>
          </div>
        </Panel>
        <Panel eyebrow="Why This Matters" title="Not another AI receptionist">
          <div className="space-y-3 text-sm text-muted">
            <p>This system is built around the operational bottleneck: safe execution inside messy clinic software.</p>
            <p>The strongest demo is cancellation recovery in a legacy EHR because it combines real revenue recovery with brittle UI automation risk.</p>
            <p>The point is not that an LLM can talk. The point is that clinic AI can execute, recover, escalate, and stay auditable.</p>
          </div>
        </Panel>
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
