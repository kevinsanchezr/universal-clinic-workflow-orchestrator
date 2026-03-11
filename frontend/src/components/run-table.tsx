import Link from "next/link";

import { StatusPill } from "@/components/ui";

export function RunTable({ runs }: { runs: Array<Record<string, unknown>> }) {
  return (
    <div className="overflow-hidden rounded-2xl border border-line">
      <table className="min-w-full text-left text-sm">
        <thead className="bg-bg text-muted">
          <tr>
            <th className="px-4 py-3">Workflow</th>
            <th className="px-4 py-3">Clinic</th>
            <th className="px-4 py-3">Status</th>
            <th className="px-4 py-3">Confidence</th>
            <th className="px-4 py-3">Step</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-line">
          {runs.map((run) => (
            <tr key={String(run.id)} className="bg-white">
              <td className="px-4 py-4 font-medium">
                <Link href={`/tasks/${String(run.id)}`} className="hover:text-accent">
                  {String(run.template_name)}
                </Link>
              </td>
              <td className="px-4 py-4">{String(run.clinic_name)}</td>
              <td className="px-4 py-4">
                <StatusPill
                  label={String(run.status)}
                  tone={run.status === "completed" ? "success" : run.status === "escalated" ? "warning" : "neutral"}
                />
              </td>
              <td className="px-4 py-4">{String(run.confidence)}%</td>
              <td className="px-4 py-4 font-mono text-xs">{String(run.current_step ?? "-")}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
