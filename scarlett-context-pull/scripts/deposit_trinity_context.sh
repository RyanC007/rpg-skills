#!/bin/bash
# =============================================================================
# Trinity Context Deposit — v6.1
# Writes the current session context to the Trinity-AI Shared Drive
#
# Drive:   Trinity-AI Shared Drive
# Drive ID: 0AMzg3SxgIv0-Uk9PVA
# Target:  02_Context_Logs/
#
# Usage:
#   bash deposit_trinity_context.sh
#   bash deposit_trinity_context.sh --topic "Morning Brief" --summary "Sent daily brief to Ryan"
#
# Arguments (all optional):
#   --topic    Short label for the session topic (default: "Session Update")
#   --summary  One-line summary of what happened (default: auto-generated)
#   --tasks    Comma-separated list of key tasks completed
#   --next     Comma-separated list of next steps
# =============================================================================

RCLONE_CONFIG="/home/ubuntu/.gdrive-rclone.ini"
TRINITY_DRIVE_ID="0AMzg3SxgIv0-Uk9PVA"
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
DATE_STR=$(date '+%Y-%m-%d')
DATE_HUMAN=$(date '+%B %-d, %Y')
TIME_HUMAN=$(date '+%I:%M %p %Z')
LOCAL_CONTEXT_DIR="/home/ubuntu/scarlett_agent_context/trinity-context"
FILE_NAME="${DATE_STR}-trinity-ryan-context.md"
LOCAL_FILE="${LOCAL_CONTEXT_DIR}/${FILE_NAME}"

# Parse optional arguments
TOPIC="Session Update"
SUMMARY="Trinity session completed. Context deposited."
TASKS=""
NEXT_STEPS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --topic) TOPIC="$2"; shift 2 ;;
    --summary) SUMMARY="$2"; shift 2 ;;
    --tasks) TASKS="$2"; shift 2 ;;
    --next) NEXT_STEPS="$2"; shift 2 ;;
    *) shift ;;
  esac
done

mkdir -p "$LOCAL_CONTEXT_DIR"

echo "============================================="
echo "  Trinity Context Deposit"
echo "  $TIMESTAMP"
echo "============================================="

# 1. Generate the context snapshot in the established format
cat > "$LOCAL_FILE" << CONTEXT_EOF
# Context Log - ${DATE_HUMAN}
**Date:** ${DATE_HUMAN}
**Time:** ${TIME_HUMAN}
**Agent:** Trinity AI - Ryan's Chief of Staff
**Protocol Version:** v6.1
**Log Type:** ${TOPIC}

---

## Session Summary
**Session Topic:** ${TOPIC}
**Summary:** ${SUMMARY}

---

## Key Activities
CONTEXT_EOF

# Append tasks if provided
if [ -n "$TASKS" ]; then
  echo "$TASKS" | tr ',' '\n' | while read -r task; do
    task=$(echo "$task" | xargs)
    [ -n "$task" ] && echo "- $task" >> "$LOCAL_FILE"
  done
else
  echo "- Trinity session executed. See summary above." >> "$LOCAL_FILE"
fi

cat >> "$LOCAL_FILE" << CONTEXT_EOF2

---

## Next Steps
CONTEXT_EOF2

# Append next steps if provided
if [ -n "$NEXT_STEPS" ]; then
  echo "$NEXT_STEPS" | tr ',' '\n' | while read -r step; do
    step=$(echo "$step" | xargs)
    [ -n "$step" ] && echo "- $step" >> "$LOCAL_FILE"
  done
else
  echo "- Monitor for Ryan's response or action confirmation" >> "$LOCAL_FILE"
  echo "- End of day: deposit updated context log" >> "$LOCAL_FILE"
fi

cat >> "$LOCAL_FILE" << CONTEXT_EOF3

---

**Log Status:** Complete
**Deposited To:** Trinity-AI Drive / 02_Context_Logs/
CONTEXT_EOF3

echo "Context snapshot generated at: $LOCAL_FILE"
echo ""

# 2. Upload to Trinity Shared Drive
echo "Uploading to Trinity-AI Shared Drive (02_Context_Logs/)..."
rclone copy "$LOCAL_FILE" \
  "manus_google_drive,drive_id=${TRINITY_DRIVE_ID},root_folder_id=${TRINITY_DRIVE_ID}:02_Context_Logs/" \
  --config "$RCLONE_CONFIG" \
  2>&1

if [ $? -eq 0 ]; then
  echo "✅ Context successfully deposited to Trinity-AI Drive / 02_Context_Logs/${FILE_NAME}"
else
  echo "❌ Error depositing context to Google Drive. Check rclone config."
  exit 1
fi
echo "============================================="
