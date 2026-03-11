"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api";
import { ClinicRecord } from "@/types";
import { Button, StatusPill } from "@/components/ui";


const defaultPayload = {
  first_name: "Luca",
  appointment_type: "Follow-up",
  preferred_date: "2026-03-11",
  callback_number: "555-3010",
  urgency: "routine",
};


function getDefaultClinic(clinics: ClinicRecord[]) {
  return clinics.find((clinic) => clinic.segment === "enterprise" && clinic.ehr_adapter.ehr_style === "legacy") ?? clinics[0] ?? null;
}


export function DemoLauncher() {
  const queryClient = useQueryClient();
  const [message, setMessage] = useState<string | null>(null);
  const [lastRun, setLastRun] = useState<{ runId: string; status: string; outcome: string | null } | null>(null);
  const [formState, setFormState] = useState(defaultPayload);

  const clinicsQuery = useQuery({
    queryKey: ["clinics"],
    queryFn: api.clinics,
  });

  const defaultClinic = useMemo(() => getDefaultClinic(clinicsQuery.data ?? []), [clinicsQuery.data]);
  const defaultUser = defaultClinic?.users.find((user) => user.role === "reviewer") ?? defaultClinic?.users[0] ?? null;

  const seedMutation = useMutation({
    mutationFn: api.seed,
    onSuccess: async (result) => {
      setMessage(result.seeded ? "Demo data seeded." : result.reason ?? "Seed skipped.");
      await queryClient.invalidateQueries({ queryKey: ["clinics"] });
      await queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    },
    onError: () => setMessage("Seed request failed."),
  });

  const launchMutation = useMutation({
    mutationFn: () => {
      if (!defaultClinic) {
        throw new Error("No demo clinic available.");
      }
      return api.launchWorkflow({
        clinic_id: defaultClinic.id,
        template_slug: "cancellation-recovery",
        requested_by_user_id: defaultUser?.id ?? null,
        ehr_style: "legacy",
        payload: formState,
      });
    },
    onSuccess: async (result) => {
      setLastRun({ runId: result.run_id, status: result.status, outcome: result.outcome });
      setMessage("Cancellation Recovery launched in LegacyEHR.");
      await queryClient.invalidateQueries({ queryKey: ["dashboard"] });
      await queryClient.invalidateQueries({ queryKey: ["runs"] });
    },
    onError: () => setMessage("Workflow launch failed. Seed the environment first and try again."),
  });

  return (
    <div className="space-y-4">
      <div className="grid gap-3 md:grid-cols-2">
        <div className="rounded-2xl border border-line bg-bg p-4">
          <p className="text-sm text-muted">Target clinic</p>
          <p className="mt-2 font-medium">{defaultClinic?.name ?? "Seed required"}</p>
          <p className="mt-1 text-sm text-muted">Segment: {defaultClinic?.segment ?? "-"}</p>
        </div>
        <div className="rounded-2xl border border-line bg-bg p-4">
          <p className="text-sm text-muted">Execution surface</p>
          <p className="mt-2 font-medium">LegacyEHR</p>
          <p className="mt-1 text-sm text-muted">Primary demo path for operational reliability</p>
        </div>
      </div>

      <div className="grid gap-3 md:grid-cols-2">
        <label className="space-y-2 text-sm">
          <span className="text-muted">Patient first name</span>
          <input
            className="w-full rounded-2xl border border-line bg-white px-4 py-3 outline-none ring-0"
            value={formState.first_name}
            onChange={(event) => setFormState((current) => ({ ...current, first_name: event.target.value }))}
          />
        </label>
        <label className="space-y-2 text-sm">
          <span className="text-muted">Callback number</span>
          <input
            className="w-full rounded-2xl border border-line bg-white px-4 py-3 outline-none ring-0"
            value={formState.callback_number}
            onChange={(event) => setFormState((current) => ({ ...current, callback_number: event.target.value }))}
          />
        </label>
        <label className="space-y-2 text-sm">
          <span className="text-muted">Appointment type</span>
          <input
            className="w-full rounded-2xl border border-line bg-white px-4 py-3 outline-none ring-0"
            value={formState.appointment_type}
            onChange={(event) => setFormState((current) => ({ ...current, appointment_type: event.target.value }))}
          />
        </label>
        <label className="space-y-2 text-sm">
          <span className="text-muted">Preferred date</span>
          <input
            className="w-full rounded-2xl border border-line bg-white px-4 py-3 outline-none ring-0"
            value={formState.preferred_date}
            onChange={(event) => setFormState((current) => ({ ...current, preferred_date: event.target.value }))}
          />
        </label>
      </div>

      <div className="flex flex-wrap gap-3">
        <Button type="button" variant="secondary" onClick={() => seedMutation.mutate()} disabled={seedMutation.isPending}>
          {seedMutation.isPending ? "Seeding..." : "Seed demo data"}
        </Button>
        <Button type="button" onClick={() => launchMutation.mutate()} disabled={launchMutation.isPending || clinicsQuery.isLoading || !defaultClinic}>
          {launchMutation.isPending ? "Launching..." : "Launch Cancellation Recovery"}
        </Button>
      </div>

      {message && <p className="text-sm text-muted">{message}</p>}

      {lastRun && (
        <div className="rounded-2xl border border-line bg-bg p-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="font-medium">Run created</p>
              <p className="mt-1 font-mono text-xs text-muted">{lastRun.runId}</p>
            </div>
            <div className="flex items-center gap-3">
              <StatusPill label={lastRun.status} tone={lastRun.status === "completed" ? "success" : "warning"} />
              <Link href={`/tasks/${lastRun.runId}`} className="text-sm font-semibold text-accent hover:underline">
                Open trace view
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
