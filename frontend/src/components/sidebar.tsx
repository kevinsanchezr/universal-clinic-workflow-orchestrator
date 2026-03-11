import Link from "next/link";

const nav = [
  ["Dashboard", "/"],
  ["Workflows", "/workflows"],
  ["Task Trace", "/tasks"],
  ["Handoff Queue", "/handoffs"],
  ["EHR Simulator", "/simulator"],
  ["Settings", "/settings"],
];

export function Sidebar() {
  return (
    <aside className="sticky top-0 flex h-screen flex-col justify-between border-r border-line bg-panel/80 p-6 backdrop-blur">
      <div>
        <div className="rounded-2xl border border-accent/20 bg-accent/5 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-accent">Clinic Ops Reliability</p>
          <h1 className="mt-2 text-xl font-semibold">Universal Workflow Orchestrator</h1>
        </div>
        <nav className="mt-8 space-y-2">
          {nav.map(([label, href]) => (
            <Link key={href} href={href} className="block rounded-2xl px-4 py-3 text-sm text-muted transition hover:bg-bg hover:text-ink">
              {label}
            </Link>
          ))}
        </nav>
      </div>
      <div className="rounded-2xl border border-line p-4 text-sm text-muted">
        <p className="font-medium text-ink">Low-PHI mode enabled</p>
        <p className="mt-2">Audit logs persist redacted summaries, confidence, retries, and outcomes.</p>
      </div>
    </aside>
  );
}
