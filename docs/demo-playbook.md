# Demo Playbook

## Seed the Environment

1. Start the stack with `docker compose up --build`
2. Seed data with `POST /api/seed`
3. Confirm templates with `POST /api/templates/sync`

## Primary Demo

Use one flow and make it excellent:

`Cancellation Recovery in LegacyEHR`

This is the highest-signal demo because it combines:

- same-day cancellation pain
- waitlist refill logic
- legacy interface execution
- confidence scoring
- human fallback
- redacted audit trace
- measurable revenue recovery

## Example Workflow Launches

### Cancellation Recovery

```json
{
  "clinic_id": "seeded summit clinic id",
  "template_slug": "cancellation-recovery",
  "ehr_style": "legacy",
  "payload": {
    "first_name": "Luca",
    "appointment_type": "Follow-up",
    "preferred_date": "2026-03-11",
    "callback_number": "555-3010",
    "urgency": "routine"
  }
}
```

Expected demo story:

1. A same-day cancellation appears in the enterprise clinic's `LegacyEHR` schedule.
2. The workflow ranks the waitlist and selects the best-fit patient.
3. The adapter reserves the slot.
4. The trace view shows each screen interaction, rationale, and confidence.
5. The dashboard displays business impact:
   - expected revenue recovered: `$180`
   - manual staff time saved: `12 minutes`
   - confidence: `0.91`
   - PHI persisted in logs: `none`

## Secondary Flows

### Appointment Booking

```json
{
  "clinic_id": "seeded harbor clinic id",
  "template_slug": "appointment-booking",
  "ehr_style": "modern",
  "payload": {
    "first_name": "Theo",
    "appointment_type": "Follow-up",
    "preferred_date": "2026-03-12",
    "callback_number": "555-2020",
    "urgency": "routine"
  }
}
```

### Prescription Refill Intake

```json
{
  "clinic_id": "seeded summit clinic id",
  "template_slug": "prescription-refill-intake",
  "ehr_style": "legacy",
  "payload": {
    "first_name": "Luca",
    "medication_name": "Atorvastatin",
    "callback_number": "555-3010",
    "urgency": "high"
  }
}
```

This flow should escalate because the policy engine marks high-urgency refill routing as ambiguous.

### Next-Day Schedule Scrub

```json
{
  "clinic_id": "seeded summit clinic id",
  "template_slug": "next-day-schedule-scrub",
  "ehr_style": "legacy",
  "payload": {
    "preferred_date": "2026-03-12",
    "urgency": "routine"
  }
}
```
