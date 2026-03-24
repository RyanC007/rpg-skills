#!/bin/bash
# =============================================================================
# Trinity Context Pull — On-Demand Script
# Use this ONLY when explicitly asked to check Trinity's context or updates.
# This script is NOT run at startup.
# =============================================================================

RCLONE_CONFIG="/home/ubuntu/.gdrive-rclone.ini"
CONTEXT_CACHE="/home/ubuntu/scarlett_agent_context"
TRINITY_DRIVE_ID="0AMzg3SxgIv0-Uk9PVA"

echo "============================================="
echo "  Trinity Context Pull — On-Demand"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================="

mkdir -p "$CONTEXT_CACHE/trinity-context"

echo ""
echo "Pulling Trinity Context Deposits..."

rclone copy \
  "manus_google_drive,drive_id=${TRINITY_DRIVE_ID},root_folder_id=${TRINITY_DRIVE_ID}:02_Context_Logs/" \
  "$CONTEXT_CACHE/trinity-context/" \
  --config "$RCLONE_CONFIG" \
  --max-age 48h \
  2>&1

TRINITY_COUNT=$(ls "$CONTEXT_CACHE/trinity-context/" 2>/dev/null | wc -l)
echo "   -> $TRINITY_COUNT Trinity context file(s) cached."

echo ""
echo "--- LATEST TRINITY CONTEXT ---"
LATEST_TRINITY=$(ls -t "$CONTEXT_CACHE/trinity-context/" 2>/dev/null | head -1)
if [ -n "$LATEST_TRINITY" ]; then
  echo "File: $LATEST_TRINITY"
  cat "$CONTEXT_CACHE/trinity-context/$LATEST_TRINITY" 2>/dev/null | head -40
else
  echo "(none found — Trinity context deposits may not yet exist for this period)"
fi

echo ""
echo "Trinity context pull complete."
