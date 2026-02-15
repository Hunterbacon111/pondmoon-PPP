#!/bin/bash
# Pondmoon PPP - One-click deploy script
# Usage: ./deploy.sh [ancora|greenwood|all]

set -e

SERVER="root@159.65.35.217"
LOCAL_BASE="$(cd "$(dirname "$0")" && pwd)"

# Correct server paths (matching Nginx config)
REMOTE_ANCORA="/var/www/dashboards/Ancora/dashboard/index.html"
REMOTE_GREENWOOD="/var/www/dashboards/Greenwood/dashboard/index.html"

deploy_ancora() {
    echo "=== Deploying Ancora ==="
    echo "  Building..."
    cd "$LOCAL_BASE/Ancora" && source .venv/bin/activate && python build.py
    echo "  Uploading to server..."
    scp "$LOCAL_BASE/Ancora/dashboard/index.html" "$SERVER:$REMOTE_ANCORA"
    echo "  ✅ Ancora deployed"
}

deploy_greenwood() {
    echo "=== Deploying Greenwood ==="
    echo "  Building..."
    cd "$LOCAL_BASE/Greenwood_At_Katy" && source .venv/bin/activate && python build.py
    echo "  Uploading to server..."
    scp "$LOCAL_BASE/Greenwood_At_Katy/dashboard/index.html" "$SERVER:$REMOTE_GREENWOOD"
    echo "  ✅ Greenwood deployed"
}

git_sync() {
    echo "=== Git sync ==="
    cd "$LOCAL_BASE"
    git add -A
    git status --short
    if git diff --cached --quiet; then
        echo "  No changes to commit"
    else
        read -p "  Commit message: " msg
        git commit -m "$msg"
        git push origin main
        ssh "$SERVER" "cd /opt/pondmoon-PPP && git pull origin main"
        echo "  ✅ Git synced"
    fi
}

case "${1:-all}" in
    ancora)
        deploy_ancora
        ;;
    greenwood)
        deploy_greenwood
        ;;
    all)
        deploy_ancora
        deploy_greenwood
        ;;
    git)
        git_sync
        ;;
    full)
        git_sync
        deploy_ancora
        deploy_greenwood
        ;;
    *)
        echo "Usage: ./deploy.sh [ancora|greenwood|all|git|full]"
        echo "  ancora    - Build & deploy Ancora only"
        echo "  greenwood - Build & deploy Greenwood only"
        echo "  all       - Build & deploy both (default)"
        echo "  git       - Git commit + push + server pull"
        echo "  full      - Git sync + build + deploy both"
        exit 1
        ;;
esac

echo ""
echo "🎉 Done!"
