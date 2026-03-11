# Contributing

## Working Model

This repository uses a lightweight trunk-based flow with short-lived branches and pull requests.

- `main` is always releasable
- Every change starts from an issue
- Every issue should produce a branch and a pull request
- Prefer small PRs with one clear objective
- Merge only after checks pass and the change is reviewed

## Branch Naming

Use one of these prefixes:

- `feat/<issue-number>-short-description`
- `fix/<issue-number>-short-description`
- `chore/<issue-number>-short-description`
- `docs/<issue-number>-short-description`

Examples:

- `feat/12-legacy-ehr-replay-mode`
- `fix/18-redaction-regression`
- `docs/21-demo-narrative-refresh`

## Commit Style

Prefer clear, imperative commits:

- `feat: add workflow replay endpoint`
- `fix: correct handoff escalation threshold`
- `docs: refine cancellation recovery demo`

## Pull Request Expectations

Every PR should include:

- the problem being solved
- the approach taken
- risks or tradeoffs
- validation performed
- screenshots for UI changes

## Engineering Guardrails

- Prefer deterministic workflow logic before using LLMs
- Do not persist raw PHI in logs, traces, or screenshots
- Keep workflow steps auditable and reversible where possible
- Preserve adapter abstractions for future EHR connectors
- Add tests for policy, redaction, and workflow state transitions when touching those areas

## Suggested Labels

- `area/backend`
- `area/frontend`
- `area/workflows`
- `area/observability`
- `area/security`
- `area/ehr-adapter`
- `kind/feature`
- `kind/bug`
- `kind/docs`
- `kind/chore`
- `priority/p0`
- `priority/p1`
- `priority/p2`
- `status/blocked`
- `status/needs-design`
- `status/ready`

## Recommended PR Flow

1. Create or refine an issue.
2. Assign scope, area, and priority labels.
3. Create a short-lived branch from `main`.
4. Open a draft PR early if the work is non-trivial.
5. Keep the PR updated with decisions and screenshots.
6. Merge with squash when the branch represents one coherent change.
