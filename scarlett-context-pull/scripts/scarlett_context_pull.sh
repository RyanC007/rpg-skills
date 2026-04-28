#!/usr/bin/env bash
# =============================================================================
# SCARLETT CONTEXT PULL — RETIRED v4.2
# This script is retired as of April 2026.
#
# It previously pulled Thor and Trinity context via rclone.
# Thor was decommissioned March 2026. Trinity has no active context deposits.
# Both agent drives returned zero files on every run since Week 17.
#
# The correct startup script is now:
#   bash /home/ubuntu/skills/scarlett-context-pull/scripts/scarlett_startup_check.sh
#
# That script reads the RPG Shared Drive context pool directly:
#   - system-knowledge (live Type 1 rules)
#   - knowledge-pending (Type 2 items awaiting Ryan review)
#   - scarlett-context-logs (last session summary)
#
# This file is kept for reference only. Do not call it.
# =============================================================================

echo "============================================="
echo "  NOTICE: scarlett_context_pull.sh is retired"
echo "  Redirecting to scarlett_startup_check.sh..."
echo "============================================="

bash /home/ubuntu/skills/scarlett-context-pull/scripts/scarlett_startup_check.sh
