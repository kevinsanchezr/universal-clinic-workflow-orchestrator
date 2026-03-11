import { api } from "@/lib/api";
import { Panel, StatusPill } from "@/components/ui";


export default async function TaskDetailPage({ params }: { params: { runId: string } }) {
  const run = await api.run(params.runId);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-accent">Trace Explorer</p>
          <h1 className="mt-2 text-3xl font-semibold">Run {run.id}</h1>
        </div>
        <div className="flex items-center gap-3">
          <StatusPill label={run.status} tone={run.status === "completed" ? "success" : run.status === "escalated" ? "warning" : "neutral"} />
          <div className="rounded-2xl border border-line px-4 py-3 text-sm">
            Confidence <span className="font-semibold">{run.confidence}%</span>
          </div>
        </div>
      </div>

      <section className="grid gap-6 xl:grid-cols-[1.4fr_1fr]">
        <Panel title="Execution steps" eyebrow={run.ehr_style}>
          <div className="space-y-4">
            {run.steps.map((step) => (
              <div key={step.id} className="rounded-2xl border border-line p-4">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="font-medium">{step.step_key}</p>
                    <p className="text-sm text-muted">{step.action_type}</p>
                  </div>
                  <StatusPill label={step.status} tone={step.status === "completed" ? "success" : step.status === "escalated" ? "warning" : "neutral"} />
                </div>
                <p className="mt-3 text-sm">{step.rationale}</p>
                <div className="mt-3 grid gap-3 md:grid-cols-3">
                  <pre className="overflow-x-auto rounded-2xl bg-bg p-3 text-xs">{JSON.stringify(step.input_summary, null, 2)}</pre>
                  <pre className="overflow-x-auto rounded-2xl bg-bg p-3 text-xs">{JSON.stringify(step.output_summary, null, 2)}</pre>
                  <pre className="overflow-x-auto rounded-2xl bg-slate-950 p-3 text-xs text-slate-100">{JSON.stringify(step.adapter_trace, null, 2)}</pre>
                </div>
              </div>
            ))}
          </div>
        </Panel>
        <Panel title="Redacted run state" eyebrow="Low-PHI view">
          <div className="space-y-4">
            <div>
              <p className="mb-2 text-sm font-medium">Input</p>
              <pre className="overflow-x-auto rounded-2xl bg-bg p-4 text-xs">{JSON.stringify(run.redacted_input, null, 2)}</pre>
            </div>
            <div>
              <p className="mb-2 text-sm font-medium">State snapshot</p>
              <pre className="overflow-x-auto rounded-2xl bg-bg p-4 text-xs">{JSON.stringify(run.state_snapshot, null, 2)}</pre>
            </div>
          </div>
        </Panel>
      </section>
    </div>
  );
}
