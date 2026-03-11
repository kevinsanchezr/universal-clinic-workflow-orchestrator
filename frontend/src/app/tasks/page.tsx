import { api } from "@/lib/api";
import { Panel } from "@/components/ui";
import { RunTable } from "@/components/run-table";


export default async function TasksPage() {
  const runs = await api.runs();

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-accent">Task Index</p>
        <h1 className="mt-2 text-3xl font-semibold">Workflow run inventory</h1>
      </div>
      <Panel title="All runs" eyebrow="Trace Entry Points">
        <RunTable runs={runs} />
      </Panel>
    </div>
  );
}
