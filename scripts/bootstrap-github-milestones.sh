#!/usr/bin/env bash

set -euo pipefail

REPO="${1:-kevinsanchezr/universal-clinic-workflow-orchestrator}"

create_milestone() {
  local title="$1"
  local description="$2"

  gh api "repos/$REPO/milestones" \
    --method POST \
    --field title="$title" \
    --field description="$description" >/dev/null 2>&1 || true
}

create_milestone "MVP Reliability" "Core execution engine, redaction, auditability, and demo workflow stability."
create_milestone "Legacy EHR Hardening" "Improve resilience of legacy adapter flows and selector fallback logic."
create_milestone "Human Handoff Operations" "Strengthen reviewer workflows, escalation handling, and queue operations."
create_milestone "Observability and Replay" "Add failure replay, richer traces, and calibration views."
create_milestone "Production Readiness" "Deployment hardening, security controls, and HIPAA-oriented operational safeguards."
