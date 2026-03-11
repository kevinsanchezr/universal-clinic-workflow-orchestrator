# Engineering Workflow

## Goal

Keep the repository ready for iterative product work without losing auditability, code quality, or delivery speed.

## Default Process

1. Open an issue before starting meaningful work.
2. Add `kind/*`, `area/*`, and `priority/*` labels.
3. Create a short-lived branch from `main`.
4. Open a draft PR for anything bigger than a small fix.
5. Merge with squash after checks pass.

## Issue Taxonomy

- `kind/feature`: product or engineering capability
- `kind/bug`: defect or regression
- `kind/docs`: documentation-only work
- `kind/chore`: maintenance work
- `area/backend`: FastAPI, models, queue, orchestration
- `area/frontend`: Next.js dashboard and UX
- `area/workflows`: templates, policy, execution rules
- `area/observability`: tracing, logging, metrics
- `area/security`: PHI, RBAC, audit, secrets
- `area/ehr-adapter`: adapter interfaces and simulator behavior

## Pull Request Standards

- Prefer one problem per PR
- Include validation evidence
- Explicitly mention PHI and audit implications if relevant
- Use screenshots for UI changes
- Note follow-up work instead of overloading the PR

## Milestone Structure

Recommended milestone progression:

1. `MVP Reliability`
2. `Legacy EHR Hardening`
3. `Human Handoff Operations`
4. `Observability and Replay`
5. `Production Readiness`

## First Useful Issues

- Add async Celery dispatch for workflow execution
- Add workflow replay mode for failed runs
- Add richer failure taxonomy and retry policy
- Add frontend launch form for primary demo workflow
- Add immutable audit export endpoint
- Add Playwright-backed simulator adapter implementation
