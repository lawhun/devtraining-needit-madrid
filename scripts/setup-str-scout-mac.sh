#!/bin/bash
# One-time setup: STR Scout Hub on your Mac
# Run once from the repo root: bash scripts/setup-str-scout-mac.sh
# After this, the hub is always at http://$(ipconfig getifaddr en0):8754/

set -euo pipefail

SCOUT_DIR="$HOME/STR-Scouts"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LAUNCHD="$HOME/Library/LaunchAgents"

echo "=== STR Scout Hub Setup ==="
echo "Repo: $REPO_DIR"
echo "Serve dir: $SCOUT_DIR"
echo ""

# 1. Create serving directory
mkdir -p "$SCOUT_DIR/logs"

# 2. Copy current HTML files
echo "→ Copying HTML files..."
cp "$REPO_DIR/index.html" "$SCOUT_DIR/"
cp "$REPO_DIR/cocoa-beach-fl-market-scout.html" "$SCOUT_DIR/"
[ -f "$REPO_DIR/gulf-shores-al-market-scout.html" ] && cp "$REPO_DIR/gulf-shores-al-market-scout.html" "$SCOUT_DIR/"
[ -f "$REPO_DIR/mansfield-tx-market-scout.html" ] && cp "$REPO_DIR/mansfield-tx-market-scout.html" "$SCOUT_DIR/"
echo "   Done."

# 3. Install HTTP server LaunchAgent (auto-starts at login, keeps running)
echo "→ Installing HTTP server LaunchAgent..."
sed "s|STR_SCOUT_DIR|$SCOUT_DIR|g" "$REPO_DIR/launchd/com.strscout.server.plist" > "$LAUNCHD/com.strscout.server.plist"
launchctl unload "$LAUNCHD/com.strscout.server.plist" 2>/dev/null || true
launchctl load "$LAUNCHD/com.strscout.server.plist"
echo "   Done."

# 4. Install daily Cocoa Beach scout LaunchAgent
echo "→ Installing Cocoa Beach daily scout LaunchAgent..."
sed "s|SCRIPTS_DIR|$REPO_DIR/scripts|g; s|HOME_DIR|$HOME|g" "$REPO_DIR/launchd/com.strscout.cocoa-beach.plist" > "$LAUNCHD/com.strscout.cocoa-beach.plist"
launchctl unload "$LAUNCHD/com.strscout.cocoa-beach.plist" 2>/dev/null || true
launchctl load "$LAUNCHD/com.strscout.cocoa-beach.plist"
echo "   Done."

# 5. Print access info
MAC_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "FIND-YOUR-IP")
echo ""
echo "=== SETUP COMPLETE ==="
echo ""
echo "Hub URL (phone + desktop):  http://$MAC_IP:8754/"
echo "Cocoa Beach direct:         http://$MAC_IP:8754/cocoa-beach-fl-market-scout.html"
echo ""
echo "Cocoa Beach scout runs daily — check ~/STR-Scouts/logs/ for output."
echo ""
echo "Add to iPhone home screen:"
echo "  Safari → open the hub URL → Share → 'Add to Home Screen' → 'STR Scout Hub'"
