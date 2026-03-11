# Architecture Notes

## Design Principles

- Rule-first orchestration for safety and repeatability
- Low-PHI persistence through input minimization and log redaction
- Strong execution observability over raw task volume
- Adapter abstraction for future EHR-specific integrations
- Human fallback as a first-class outcome, not an exception

## Reliability Strategy

- Workflow templates declare preconditions, retries, and handoff rules
- Execution state is persisted as structured run and step records
- EHR adapters support selector-first automation with semantic fallback
- Policy engine emits confidence, rationale, and escalation flags per step
- Failures are categorized for retry, escalation, or terminal stop

## PHI Strategy

- Structured task inputs classify fields by sensitivity
- Logs store redacted payloads and summaries, not full source values
- Simulated patient data uses pseudonymous demo fixtures
- Secrets remain environment-based and excluded from application logs
