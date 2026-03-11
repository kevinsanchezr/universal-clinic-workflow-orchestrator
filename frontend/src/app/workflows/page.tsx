import { api } from "@/lib/api";
import { Panel } from "@/components/ui";


export default async function WorkflowsPage() {
  const templates = await api.templates();

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-accent">Reusable Templates</p>
        <h1 className="mt-2 text-3xl font-semibold">Workflow builder preview</h1>
      </div>
      <div className="grid gap-6 xl:grid-cols-2">
        {templates.map((template) => (
          <Panel key={String(template.id)} title={String(template.name)} eyebrow={String(template.slug)}>
            <pre className="overflow-x-auto rounded-2xl bg-slate-950 p-4 text-xs text-slate-100">
              {JSON.stringify(template.definition, null, 2)}
            </pre>
          </Panel>
        ))}
      </div>
    </div>
  );
}
