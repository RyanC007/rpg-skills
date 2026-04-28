#!/usr/bin/env bash
# =============================================================================
# SCARLETT SESSION ACTIVITY LOGGER — v1.1
# Appends an activity entry to the current session's Drive log.
# Call mid-task to record what Scarlett did, decided, or discovered.
# =============================================================================
# USAGE:
#   bash scarlett_log_activity.sh "Brief description of what happened"
# =============================================================================

DRIVE_ID="0AK8dAs_XgfnNUk9PVA"
WORK_DIR="/home/ubuntu/.scarlett_session_work"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
ACTIVITY_TEXT="${1:-No activity description provided}"

SESSION_FILE_ID=$(cat "$WORK_DIR/current_session_id" 2>/dev/null || echo "")
SESSION_NAME=$(cat "$WORK_DIR/current_session_name" 2>/dev/null || echo "unknown_session")

if [ -z "$SESSION_FILE_ID" ]; then
  echo "!! No active session ID found. Run scarlett_startup_check.sh first."
  exit 1
fi

mkdir -p "$WORK_DIR"

# Download current log
gws drive files get \
  --params "{\"fileId\":\"$SESSION_FILE_ID\",\"supportsAllDrives\":true,\"alt\":\"media\"}" \
  --output "$WORK_DIR/current_log.md" 2>/dev/null

# Append new entry
cat >> "$WORK_DIR/current_log.md" << EOF

### [$TIMESTAMP] Activity
$ACTIVITY_TEXT
EOF

# Upload updated log back to Drive
gws drive files update \
  --params "{\"fileId\":\"$SESSION_FILE_ID\",\"supportsAllDrives\":true}" \
  --upload "$WORK_DIR/current_log.md" \
  --upload-content-type "text/markdown" \
  2>/dev/null

# Clean up local copy
rm -f "$WORK_DIR/current_log.md"

echo "-> Activity logged to Drive session: $SESSION_NAME"
