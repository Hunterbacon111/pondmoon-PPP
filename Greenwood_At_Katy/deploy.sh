#!/bin/bash
# Greenwood at Katy - One-click deploy: upload data → build on server → dashboard updated
set -e

SERVER="root@159.65.35.217"
REMOTE_DIR="/var/www/dashboards/Greenwood"
LOCAL_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================"
echo "  Greenwood at Katy - Deploy to Server"
echo "============================================"

# Step 1: Upload data files + scripts
echo ""
echo "[1/3] Uploading data files..."
scp "$LOCAL_DIR/extract_single.py" "$SERVER:$REMOTE_DIR/"
scp -r "$LOCAL_DIR/Data_Annual_Budget" "$SERVER:$REMOTE_DIR/"
scp -r "$LOCAL_DIR/Data_Comps" "$SERVER:$REMOTE_DIR/"
scp -r "$LOCAL_DIR/Data_Financials" "$SERVER:$REMOTE_DIR/"
scp -r "$LOCAL_DIR/Data_HUDLoan" "$SERVER:$REMOTE_DIR/"
scp -r "$LOCAL_DIR/Data_Leasing" "$SERVER:$REMOTE_DIR/"
scp -r "$LOCAL_DIR/Data_Minutes" "$SERVER:$REMOTE_DIR/"
scp -r "$LOCAL_DIR/Data_Marketing_Others" "$SERVER:$REMOTE_DIR/" 2>/dev/null || true
scp -r "$LOCAL_DIR/Data_Project Information" "$SERVER:$REMOTE_DIR/"
scp -r "$LOCAL_DIR/Data_T12P&L" "$SERVER:$REMOTE_DIR/" 2>/dev/null || true
echo "  Done."

# Step 2: Build on server
echo ""
echo "[2/3] Building dashboard on server..."
ssh "$SERVER" "cd $REMOTE_DIR && source .venv/bin/activate && python3 build.py"

# Step 3: Verify
echo ""
echo "[3/3] Verifying..."
SIZE=$(ssh "$SERVER" "stat -c%s $REMOTE_DIR/dashboard/index.html 2>/dev/null || echo 0")
echo "  Dashboard size: $(( SIZE / 1024 )) KB"

echo ""
echo "============================================"
echo "  Done! Visit: http://159.65.35.217/greenwood/"
echo "============================================"
