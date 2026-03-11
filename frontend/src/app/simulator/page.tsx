import { api } from "@/lib/api";
import { Panel, StatusPill } from "@/components/ui";


export default async function SimulatorPage() {
  const simulators = await api.simulators();

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-accent">UI Automation Surface</p>
        <h1 className="mt-2 text-3xl font-semibold">EHR simulator</h1>
      </div>
      <div className="grid gap-6 xl:grid-cols-2">
        {simulators.map((simulator) => (
          <Panel key={String(simulator.clinic_id)} title={String(simulator.clinic_name)} eyebrow={String(simulator.ehr_style)}>
            <div className="grid gap-4 xl:grid-cols-2">
              <div className="rounded-2xl border border-line bg-bg p-4">
                <p className="mb-3 text-sm font-medium">Patients</p>
                <div className="space-y-3">
                  {(simulator.patients as Array<Record<string, unknown>>).map((patient) => (
                    <div key={String(patient.id)} className="rounded-2xl border border-line bg-white p-3">
                      <p className="font-medium">{String(patient.pseudonym)}</p>
                      <p className="text-sm text-muted">
                        Waitlist: <span className="font-medium">{String(patient.is_waitlist)}</span>
                      </p>
                    </div>
                  ))}
                </div>
              </div>
              <div className="rounded-2xl border border-line bg-slate-950 p-4 text-slate-100">
                <p className="mb-3 text-sm font-medium">Appointment surface</p>
                <div className="space-y-3">
                  {(simulator.slots as Array<Record<string, unknown>>).map((slot) => (
                    <div key={String(slot.id)} className="rounded-2xl border border-white/10 p-3">
                      <div className="flex items-center justify-between gap-3">
                        <p className="font-medium">{String(slot.start_at)}</p>
                        <StatusPill
                          label={String(slot.status)}
                          tone={slot.status === "open" ? "neutral" : slot.status === "cancelled" ? "danger" : "success"}
                        />
                      </div>
                      <p className="mt-2 text-sm text-slate-300">{String(slot.visit_type)}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </Panel>
        ))}
      </div>
    </div>
  );
}
