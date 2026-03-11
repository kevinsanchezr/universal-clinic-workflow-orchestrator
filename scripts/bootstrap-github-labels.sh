#!/usr/bin/env bash

set -euo pipefail

REPO="${1:-kevinsanchezr/universal-clinic-workflow-orchestrator}"

create_label() {
  local name="$1"
  local color="$2"
  local description="$3"

  gh label create "$name" --repo "$REPO" --color "$color" --description "$description" 2>/dev/null \
    || gh label edit "$name" --repo "$REPO" --color "$color" --description "$description"
}

create_label "kind/feature" "1d76db" "New capability or product functionality"
create_label "kind/bug" "d73a4a" "Defect, regression, or broken behavior"
create_label "kind/docs" "0e8a16" "Documentation-only work"
create_label "kind/chore" "6f42c1" "Maintenance or non-user-facing work"
create_label "area/backend" "5319e7" "Backend, orchestration, models, APIs"
create_label "area/frontend" "fbca04" "Dashboard, UX, or frontend implementation"
create_label "area/workflows" "0052cc" "Workflow templates, policy, and execution logic"
create_label "area/observability" "006b75" "Tracing, metrics, and failure analysis"
create_label "area/security" "b60205" "PHI, audit, RBAC, and security controls"
create_label "area/ehr-adapter" "c2e0c6" "EHR adapters, simulators, and UI automation"
create_label "priority/p0" "b60205" "Highest priority"
create_label "priority/p1" "d93f0b" "Important, next up"
create_label "priority/p2" "fbca04" "Valuable but not urgent"
create_label "status/blocked" "000000" "Blocked by dependency or external constraint"
create_label "status/needs-design" "f9d0c4" "Needs product or technical design clarification"
create_label "status/ready" "0e8a16" "Ready to implement"

