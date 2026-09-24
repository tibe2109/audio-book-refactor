#!/usr/bin/env bash
# ==============================================================================
# ABV-04: Daily Automated YouTube Uploader Cron Runner
# Runs automatically every day after 15:00 VN until all 120 videos are uploaded.
# ==============================================================================
set -e

PROJECT_ROOT="/media/hoanganh/disk1_vol1/Solution/audio-book-refactor"
PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python"
UPLOADER_SCRIPT="$PROJECT_ROOT/core/abv_youtube_uploader.py"
SOURCE_DIR="$PROJECT_ROOT/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia"
THUMBNAIL_FILE="$PROJECT_ROOT/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/Final-Tam-Quoc-Dien-Nghia/backgrounds/Background-1_thumb.jpg"
LOG_FILE="$PROJECT_ROOT/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/Final-Tam-Quoc-Dien-Nghia/Videos/daily_upload.log"
MANIFEST_FILE="$PROJECT_ROOT/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/Final-Tam-Quoc-Dien-Nghia/Videos/.abv_upload_manifest.json"

echo "=======================================================" >> "$LOG_FILE"
echo "🕒 [$(date '+%Y-%m-%d %H:%M:%S')] Starting Daily YouTube Batch Upload..." >> "$LOG_FILE"
echo "=======================================================" >> "$LOG_FILE"

# Check if manifest exists and if all videos are already uploaded
if [ -f "$MANIFEST_FILE" ]; then
    TOTAL=$("$PYTHON_BIN" -c "import json; m=json.load(open('$MANIFEST_FILE')); print(m.get('total_videos', 0))" 2>/dev/null || echo 0)
    UPLOADED=$("$PYTHON_BIN" -c "import json; m=json.load(open('$MANIFEST_FILE')); print(m.get('uploaded_count', 0))" 2>/dev/null || echo 0)
    
    if [ "$TOTAL" -gt 0 ] && [ "$UPLOADED" -ge "$TOTAL" ]; then
        echo "🎉 [COMPLETE] All $TOTAL videos have been successfully uploaded to YouTube! Exiting." >> "$LOG_FILE"
        exit 0
    fi
    echo "📊 Status before upload: $UPLOADED / $TOTAL uploaded." >> "$LOG_FILE"
fi

# Execute upload with automatic quota handling, playlist sync, and public status
cd "$PROJECT_ROOT"
"$PYTHON_BIN" "$UPLOADER_SCRIPT" \
    --source "$SOURCE_DIR" \
    --thumbnail "$THUMBNAIL_FILE" \
    --batch_start 1 \
    --batch_end 120 \
    --sync_playlist \
    --set_privacy public >> "$LOG_FILE" 2>&1 || true

echo "🕒 [$(date '+%Y-%m-%d %H:%M:%S')] Daily YouTube Batch Upload session completed." >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
