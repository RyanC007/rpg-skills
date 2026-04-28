#!/usr/bin/env bash
# =============================================================================
# SCARLETT KNOWLEDGE UPDATE — v1.1
# Writes new knowledge directly to the RPG Shared Drive.
# Type 1 (System) -> system-knowledge folder (live, no review needed)
# Type 2 (Entity) -> knowledge-pending folder (staged for Ryan's review)
# Also appends a record to the current session log.
# =============================================================================
# USAGE:
#   bash scarlett_knowledge_update.sh \
#     --type 1 \
#     --title "manus-api-chatgpt-integration" \
#     --content "Full markdown content of the knowledge update"
#
#   --type   : 1 = System Knowledge (live), 2 = Entity Knowledge (pending review)
#   --title  : Short slug used as filename (no spaces, use hyphens)
#   --content: Full markdown text of the knowledge update
# =============================================================================

DRIVE_ID="0AK8dAs_XgfnNUk9PVA"
SYSTEM_KNOWLEDGE_FOLDER="1xYW5dA14c_jPIZ3XXOcc7qz0fddjt61h"
KNOWLEDGE_PENDING_FOLDER="1ZxlDrK8sxbvtuLp3e4jIgSTvWXYB1XAI"
WORK_DIR="/home/ubuntu/.scarlett_session_work"
DATE=$(date '+%Y-%m-%d')
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

mkdir -p "$WORK_DIR"

# Parse args
TYPE=""
TITLE=""
CONTENT=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --type) TYPE="$2"; shift 2 ;;
    --title) TITLE="$2"; shift 2 ;;
    --content) CONTENT="$2"; shift 2 ;;
    *) shift ;;
  esac
done

if [ -z "$TYPE" ] || [ -z "$TITLE" ] || [ -z "$CONTENT" ]; then
  echo "!! ERROR: --type, --title, and --content are all required."
  exit 1
fi

# Determine target folder and filename
if [ "$TYPE" = "1" ]; then
  TARGET_FOLDER="$SYSTEM_KNOWLEDGE_FOLDER"
  FILENAME="system-knowledge_${TITLE}_${DATE}.md"
  DEST_LABEL="system-knowledge (LIVE)"
elif [ "$TYPE" = "2" ]; then
  TARGET_FOLDER="$KNOWLEDGE_PENDING_FOLDER"
  FILENAME="knowledge-pending_${TITLE}_${DATE}.md"
  DEST_LABEL="knowledge-pending (AWAITING RYAN REVIEW)"
else
  echo "!! ERROR: --type must be 1 (System) or 2 (Entity/Pending)."
  exit 1
fi

SESSION_NAME=$(cat "$WORK_DIR/current_session_name" 2>/dev/null || echo "unknown")

# Write content to work dir
cat > "$WORK_DIR/$FILENAME" << EOF
# Knowledge Update: $TITLE
**Type:** $([ "$TYPE" = "1" ] && echo "System Knowledge (Type 1)" || echo "Entity Knowledge (Type 2 — Pending Review)")
**Date:** $DATE
**Agent:** Scarlett v6.1
**Session:** $SESSION_NAME

---

$CONTENT
EOF

# Upload to Drive
UPLOAD_RESULT=$(gws drive files create \
  --params '{"supportsAllDrives":true}' \
  --json "{\"name\":\"$FILENAME\",\"parents\":[\"$TARGET_FOLDER\"],\"mimeType\":\"text/markdown\"}" \
  --upload "$WORK_DIR/$FILENAME" \
  --upload-content-type "text/markdown" \
  2>&1)

FILE_ID=$(echo "$UPLOAD_RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('id','ERROR'))" 2>/dev/null || echo "ERROR")

# Clean up local copy immediately
rm -f "$WORK_DIR/$FILENAME"

if [ "$FILE_ID" != "ERROR" ]; then
  echo "-> Knowledge update written to Drive:"
  echo "   File  : $FILENAME"
  echo "   Dest  : $DEST_LABEL"
  echo "   ID    : $FILE_ID"

  # Log this to the session log
  SESSION_FILE_ID=$(cat "$WORK_DIR/current_session_id" 2>/dev/null || echo "")
  if [ -n "$SESSION_FILE_ID" ]; then
    gws drive files get \
      --params "{\"fileId\":\"$SESSION_FILE_ID\",\"supportsAllDrives\":true,\"alt\":\"media\"}" \
      --output "$WORK_DIR/session_log.md" 2>/dev/null || true

    if [ -f "$WORK_DIR/session_log.md" ]; then
      cat >> "$WORK_DIR/session_log.md" << EOF

### [$TIMESTAMP] Knowledge Update Written
- **File:** $FILENAME
- **Destination:** $DEST_LABEL
- **Drive ID:** $FILE_ID
EOF
      gws drive files update \
        --params "{\"fileId\":\"$SESSION_FILE_ID\",\"supportsAllDrives\":true}" \
        --upload "$WORK_DIR/session_log.md" \
        --upload-content-type "text/markdown" \
        2>/dev/null
      rm -f "$WORK_DIR/session_log.md"
    fi
  fi

  if [ "$TYPE" = "2" ]; then
    echo ""
    echo "!! REVIEW FLAG: Entity knowledge staged in knowledge-pending."
    echo "   Say 'review pending knowledge' when ready to commit."
  fi
else
  echo "!! ERROR: Failed to upload knowledge update to Drive."
  echo "$UPLOAD_RESULT"
  exit 1
fi
