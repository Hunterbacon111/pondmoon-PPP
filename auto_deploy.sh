#!/bin/bash
# Auto-deploy watcher: monitors Data_* folders, triggers deploy on changes
# Usage:
#   ./auto_deploy.sh          # Start monitoring (runs in foreground)
#   ./auto_deploy.sh start    # Start monitoring in background
#   ./auto_deploy.sh stop     # Stop background monitoring

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$BASE_DIR/.auto_deploy.pid"
LOG_FILE="$BASE_DIR/auto_deploy.log"

# Directories to watch
ANCORA_DIR="$BASE_DIR/Ancora"
GREENWOOD_DIR="$BASE_DIR/Greenwood_At_Katy"

# Cooldown: wait 30 seconds after a change before deploying
# (in case multiple files are being copied at once)
COOLDOWN=30

# Check interval (seconds)
CHECK_INTERVAL=10

# --- Helper functions ---
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

get_fingerprint() {
    local dir="$1"
    # Get modification times of all files in Data_* directories
    find "$dir"/Data_* -type f 2>/dev/null | sort | xargs stat -f "%m %N" 2>/dev/null | md5
}

deploy_project() {
    local project="$1"
    local script="$2"
    log ">>> Deploying $project..."
    if bash "$script" >> "$LOG_FILE" 2>&1; then
        log ">>> $project deployed successfully!"
        # macOS notification
        osascript -e "display notification \"$project dashboard updated\" with title \"PPP Auto-Deploy\"" 2>/dev/null || true
    else
        log ">>> ERROR: $project deploy failed!"
        osascript -e "display notification \"$project deploy FAILED\" with title \"PPP Auto-Deploy\" sound name \"Basso\"" 2>/dev/null || true
    fi
}

# --- Commands ---
case "${1:-run}" in
    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                kill "$PID"
                rm "$PID_FILE"
                echo "Auto-deploy stopped (PID $PID)"
            else
                rm "$PID_FILE"
                echo "Process already stopped"
            fi
        else
            echo "No running auto-deploy found"
        fi
        exit 0
        ;;
    start)
        if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            echo "Auto-deploy already running (PID $(cat "$PID_FILE"))"
            exit 1
        fi
        nohup "$0" run >> "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        echo "Auto-deploy started in background (PID $!)"
        echo "Log file: $LOG_FILE"
        exit 0
        ;;
    run)
        ;;
    *)
        echo "Usage: $0 [start|stop|run]"
        exit 1
        ;;
esac

# --- Main monitoring loop ---
log "=== Auto-deploy watcher started ==="
log "Monitoring:"
log "  Ancora:   $ANCORA_DIR/Data_*"
log "  Greenwood: $GREENWOOD_DIR/Data_*"
log "Check interval: ${CHECK_INTERVAL}s, Cooldown: ${COOLDOWN}s"

# Initial fingerprints
ANCORA_FP=$(get_fingerprint "$ANCORA_DIR")
GREENWOOD_FP=$(get_fingerprint "$GREENWOOD_DIR")

ANCORA_CHANGED=0
GREENWOOD_CHANGED=0
ANCORA_CHANGE_TIME=0
GREENWOOD_CHANGE_TIME=0

while true; do
    sleep "$CHECK_INTERVAL"

    NOW=$(date +%s)

    # Check Ancora
    NEW_FP=$(get_fingerprint "$ANCORA_DIR")
    if [ "$NEW_FP" != "$ANCORA_FP" ]; then
        if [ "$ANCORA_CHANGED" -eq 0 ]; then
            log "Change detected in Ancora data files, waiting ${COOLDOWN}s..."
        fi
        ANCORA_CHANGED=1
        ANCORA_CHANGE_TIME=$NOW
        ANCORA_FP="$NEW_FP"
    fi

    # Check Greenwood
    NEW_FP=$(get_fingerprint "$GREENWOOD_DIR")
    if [ "$NEW_FP" != "$GREENWOOD_FP" ]; then
        if [ "$GREENWOOD_CHANGED" -eq 0 ]; then
            log "Change detected in Greenwood data files, waiting ${COOLDOWN}s..."
        fi
        GREENWOOD_CHANGED=1
        GREENWOOD_CHANGE_TIME=$NOW
        GREENWOOD_FP="$NEW_FP"
    fi

    # Deploy after cooldown
    if [ "$ANCORA_CHANGED" -eq 1 ] && [ $(( NOW - ANCORA_CHANGE_TIME )) -ge "$COOLDOWN" ]; then
        ANCORA_CHANGED=0
        deploy_project "Ancora" "$ANCORA_DIR/deploy.sh"
        ANCORA_FP=$(get_fingerprint "$ANCORA_DIR")
    fi

    if [ "$GREENWOOD_CHANGED" -eq 1 ] && [ $(( NOW - GREENWOOD_CHANGE_TIME )) -ge "$COOLDOWN" ]; then
        GREENWOOD_CHANGED=0
        deploy_project "Greenwood" "$GREENWOOD_DIR/deploy.sh"
        GREENWOOD_FP=$(get_fingerprint "$GREENWOOD_DIR")
    fi
done
