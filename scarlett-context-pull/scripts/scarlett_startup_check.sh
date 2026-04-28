#!/usr/bin/env bash
# =============================================================================
# SCARLETT STARTUP CONTEXT-POOL CHECK — v1.1
# Runs at the start of every Scarlett task.
# Reads the RPG Shared Drive context pool ONLY (no Thor, no Trinity).
# Checks for pending knowledge updates and surfaces them for review.
# Writes a startup entry to the session log on Drive.
# =============================================================================
# PROTOCOL: Drive-First. Zero local-only storage.
# All reads come from Drive. All writes go to Drive.
# Work files use ~/.scarlett_session_work/ (auto-cleaned after upload).
# =============================================================================

set -e

# --- CONFIG ------------------------------------------------------------------
DRIVE_ID="0AK8dAs_XgfnNUk9PVA"
SYSTEM_KNOWLEDGE_FOLDER="1xYW5dA14c_jPIZ3XXOcc7qz0fddjt61h"
KNOWLEDGE_PENDING_FOLDER="1ZxlDrK8sxbvtuLp3e4jIgSTvWXYB1XAI"
CONTEXT_LOGS_FOLDER="1qI_vetE2cKzy8jcY_ivVefZezcrsGZeK"
WORK_DIR="/home/ubuntu/.scarlett_session_work"
SESSION_DATE=$(date '+%Y-%m-%d')
SESSION_TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
SESSION_ID="scarlett_session_${SESSION_DATE}_$(date '+%H%M%S')"

mkdir -p "$WORK_DIR"

echo "============================================="
echo "  SCARLETT STARTUP CHECK — v1.1"
echo "  $SESSION_TIMESTAMP"
echo "  Session ID: $SESSION_ID"
echo "============================================="

# --- STEP 1: READ SYSTEM KNOWLEDGE -------------------------------------------
echo ""
echo "[1/3] Reading system-knowledge from Drive..."

SYSTEM_FILES=$(gws drive files list \
  --params "{\"driveId\":\"$DRIVE_ID\",\"supportsAllDrives\":true,\"includeItemsFromAllDrives\":true,\"corpora\":\"drive\",\"q\":\"\\\"$SYSTEM_KNOWLEDGE_FOLDER\\\" in parents and mimeType='text/markdown'\",\"orderBy\":\"modifiedTime desc\",\"fields\":\"files(id,name,modifiedTime)\"}" \
  2>/dev/null)

SYS_COUNT=$(echo "$SYSTEM_FILES" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('files',[])))" 2>/dev/null || echo "0")
LATEST_SYS=$(echo "$SYSTEM_FILES" | python3 -c "import json,sys; d=json.load(sys.stdin); f=d.get('files',[]); print(f[0]['name'] if f else 'none')" 2>/dev/null || echo "none")

echo "   -> $SYS_COUNT system-knowledge file(s) found."
echo "   -> Latest: $LATEST_SYS"

# --- STEP 2: CHECK KNOWLEDGE-PENDING -----------------------------------------
echo ""
echo "[2/3] Checking knowledge-pending for unreviewed updates..."

PENDING_FILES=$(gws drive files list \
  --params "{\"driveId\":\"$DRIVE_ID\",\"supportsAllDrives\":true,\"includeItemsFromAllDrives\":true,\"corpora\":\"drive\",\"q\":\"\\\"$KNOWLEDGE_PENDING_FOLDER\\\" in parents and mimeType='text/markdown'\",\"orderBy\":\"modifiedTime desc\",\"fields\":\"files(id,name,modifiedTime)\"}" \
  2>/dev/null)

PENDING_COUNT=$(echo "$PENDING_FILES" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('files',[])))" 2>/dev/null || echo "0")
PENDING_NAMES=$(echo "$PENDING_FILES" | python3 -c "
import json,sys
d=json.load(sys.stdin)
files=d.get('files',[])
for f in files:
    print('   PENDING: ' + f['name'] + ' (modified: ' + f['modifiedTime'][:10] + ')')
" 2>/dev/null || echo "   (none)")

if [ "$PENDING_COUNT" -gt "0" ]; then
  echo "   !! $PENDING_COUNT PENDING knowledge update(s) awaiting Ryan's review:"
  echo "$PENDING_NAMES"
  PENDING_FLAG="YES — $PENDING_COUNT item(s) in knowledge-pending"
else
  echo "   -> No pending knowledge updates. All clear."
  PENDING_FLAG="None"
fi

# --- STEP 3: READ MOST RECENT CONTEXT LOG ------------------------------------
echo ""
echo "[3/3] Reading most recent Scarlett context log from Drive..."

RECENT_LOGS=$(gws drive files list \
  --params "{\"driveId\":\"$DRIVE_ID\",\"supportsAllDrives\":true,\"includeItemsFromAllDrives\":true,\"corpora\":\"drive\",\"q\":\"\\\"$CONTEXT_LOGS_FOLDER\\\" in parents and mimeType='text/markdown'\",\"orderBy\":\"modifiedTime desc\",\"fields\":\"files(id,name,modifiedTime)\"}" \
  2>/dev/null)

LAST_LOG_NAME=$(echo "$RECENT_LOGS" | python3 -c "import json,sys; d=json.load(sys.stdin); f=d.get('files',[]); print(f[0]['name'] if f else 'none')" 2>/dev/null || echo "none")
LAST_LOG_ID=$(echo "$RECENT_LOGS" | python3 -c "import json,sys; d=json.load(sys.stdin); f=d.get('files',[]); print(f[0]['id'] if f else 'none')" 2>/dev/null || echo "none")

if [ "$LAST_LOG_ID" != "none" ]; then
  echo "   -> Last session log: $LAST_LOG_NAME"
  gws drive files get \
    --params "{\"fileId\":\"$LAST_LOG_ID\",\"supportsAllDrives\":true,\"alt\":\"media\"}" \
    --output "$WORK_DIR/last_log.md" 2>/dev/null || true

  if [ -f "$WORK_DIR/last_log.md" ]; then
    echo ""
    echo "--- LAST SESSION SUMMARY (tail) ---"
    tail -20 "$WORK_DIR/last_log.md"
    echo "--- END ---"
    rm -f "$WORK_DIR/last_log.md"
  fi
else
  echo "   -> No previous context logs found. This is the first session."
  LAST_LOG_NAME="none"
fi

# --- WRITE STARTUP ENTRY TO DRIVE --------------------------------------------
echo ""
echo "[Writing startup session log to Drive...]"

cat > "$WORK_DIR/${SESSION_ID}.md" << LOGEOF
# Scarlett Session Log — $SESSION_DATE
**Session ID:** $SESSION_ID
**Started:** $SESSION_TIMESTAMP
**Agent:** Scarlett v6.1
**Drive:** RPG Shared Drive ($DRIVE_ID)

## Startup Check Results
| Check | Result |
|:---|:---|
| System Knowledge Files | $SYS_COUNT file(s) found, latest: $LATEST_SYS |
| Knowledge Pending | $PENDING_FLAG |
| Last Session Log | $LAST_LOG_NAME |

## Session Activity Log
_(Updates appended during session)_

LOGEOF

UPLOAD_RESULT=$(gws drive files create \
  --params '{"supportsAllDrives":true}' \
  --json "{\"name\":\"${SESSION_ID}.md\",\"parents\":[\"$CONTEXT_LOGS_FOLDER\"],\"mimeType\":\"text/markdown\"}" \
  --upload "$WORK_DIR/${SESSION_ID}.md" \
  --upload-content-type "text/markdown" \
  2>&1)

SESSION_FILE_ID=$(echo "$UPLOAD_RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('id','ERROR'))" 2>/dev/null || echo "ERROR")

if [ "$SESSION_FILE_ID" != "ERROR" ]; then
  echo "   -> Session log created on Drive: ${SESSION_ID}.md"
  echo "   -> Drive File ID: $SESSION_FILE_ID"
  # Store session state in work dir (not /tmp) for other scripts
  echo "$SESSION_FILE_ID" > "$WORK_DIR/current_session_id"
  echo "$SESSION_ID" > "$WORK_DIR/current_session_name"
  # Remove the uploaded file locally
  rm -f "$WORK_DIR/${SESSION_ID}.md"
else
  echo "   !! WARNING: Could not write session log to Drive."
  echo "$UPLOAD_RESULT"
fi

# --- SUMMARY -----------------------------------------------------------------
echo ""
echo "============================================="
echo "  STARTUP CHECK COMPLETE"
echo "  System Knowledge : $SYS_COUNT file(s)"
echo "  Pending Updates  : $PENDING_FLAG"
echo "  Session Log ID   : $SESSION_FILE_ID"
echo "============================================="

if [ "$PENDING_COUNT" -gt "0" ]; then
  echo ""
  echo "!! ACTION REQUIRED: $PENDING_COUNT knowledge update(s) staged in"
  echo "   knowledge-pending await Ryan's review."
  echo "   Say 'review pending knowledge' when ready."
fi

echo ""
echo "Scarlett is context-aware and ready. Proceeding with task."
