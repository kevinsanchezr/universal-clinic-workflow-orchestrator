import { api } from "@/lib/api";
import { Panel, StatusPill } from "@/components/ui";


export default async function HandoffsPage() {
  const handoffs = await api.handoffs();

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-accent">Human In The Loop</p>
        <h1 className="mt-2 text-3xl font-semibold">Handoff queue</h1>
      </div>
      <Panel title="Open escalations" eyebrow="Reviewer workbench">
        <div className="space-y-4">
          {handoffs.map((item) => (
            <div key={String(item.id)} className="grid gap-4 rounded-2xl border border-line p-4 xl:grid-cols-[160px_1fr_1fr]">
              <div className="space-y-2">
                <StatusPill label={String(item.priority)} tone="warning" />
                <p className="text-xs text-muted">{new Date(String(item.created_at)).toLocaleString()}</p>
              </div>
              <div>
                <p className="font-medium">{String(item.reason)}</p>
                <p className="mt-2 text-sm text-muted">Run ID: {String(item.workflow_run_id)}</p>
              </div>
              <pre className="overflow-x-auto rounded-2xl bg-bg p-3 text-xs">{JSON.stringify(item.redacted_context, null, 2)}</pre>
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
}
