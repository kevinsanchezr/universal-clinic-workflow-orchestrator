import { api } from "@/lib/api";
import { Panel } from "@/components/ui";


export default async function SettingsPage() {
  const settings = await api.settings();

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-accent">Security Controls</p>
        <h1 className="mt-2 text-3xl font-semibold">Settings and roles</h1>
      </div>
      <section className="grid gap-6 xl:grid-cols-2">
        <Panel title="RBAC policy" eyebrow="Access Model">
          <pre className="overflow-x-auto rounded-2xl bg-bg p-4 text-xs">{JSON.stringify(settings.rbac_policy, null, 2)}</pre>
        </Panel>
        <Panel title="Available roles" eyebrow="Supervisor Controls">
          <div className="space-y-3">
            {(settings.roles as string[]).map((role) => (
              <div key={role} className="rounded-2xl border border-line p-4 font-medium">
                {role}
              </div>
            ))}
          </div>
        </Panel>
      </section>
    </div>
  );
}
