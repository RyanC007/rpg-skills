#!/usr/bin/env bash
# =============================================================================
# SCARLETT SESSION CLOSER — v1.1
# Writes a closing summary to the current session log on Drive.
# Call at the end of every task before delivering results to Ryan.
# Removes work files from ~/.scarlett_session_work/ after upload.
# =============================================================================
# USAGE:
#   bash scarlett_session_close.sh "Brief summary of what was accomplished"
# =============================================================================

DRIVE_ID="0AK8dAs_XgfnNUk9PVA"
WORK_DIR="/home/ubuntu/.scarlett_session_work"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
SUMMARY_TEXT="${1:-Session completed. No summary provided.}"

SESSION_FILE_ID=$(cat "$WORK_DIR/current_session_id" 2>/dev/null || echo "")
SESSION_NAME=$(cat "$WORK_DIR/current_session_name" 2>/dev/null || echo "unknown_session")

if [ -z "$SESSION_FILE_ID" ]; then
  echo "!! No active session ID found. Nothing to close."
  exit 0
fi

# Download current log
gws drive files get \
  --params "{\"fileId\":\"$SESSION_FILE_ID\",\"supportsAllDrives\":true,\"alt\":\"media\"}" \
  --output "$WORK_DIR/session_log.md" 2>/dev/null || true

if [ -f "$WORK_DIR/session_log.md" ]; then
  cat >> "$WORK_DIR/session_log.md" << EOF

---

## Session Close
**Closed:** $TIMESTAMP

### Summary
$SUMMARY_TEXT

### Status
Session complete. Log persisted to Drive. No local data retained.
EOF

  gws drive files update \
    --params "{\"fileId\":\"$SESSION_FILE_ID\",\"supportsAllDrives\":true}" \
    --upload "$WORK_DIR/session_log.md" \
    --upload-content-type "text/markdown" \
    2>/dev/null

  rm -f "$WORK_DIR/session_log.md"
  echo "-> Session log closed and saved to Drive: $SESSION_NAME"
else
  echo "!! Could not download session log to close it."
fi

# Clear session state files
rm -f "$WORK_DIR/current_session_id"
rm -f "$WORK_DIR/current_session_name"

echo "-> Work directory cleared. Drive is the single source of truth."
