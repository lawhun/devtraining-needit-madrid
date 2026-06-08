#!/bin/bash
# Migrate all STR scouts from port 8753 to port 8754 (unified hub)
# Finds the 8753 serving directory, copies files to ~/STR-Scouts, stops old server

set -euo pipefail

SCOUT_DIR="$HOME/STR-Scouts"
LAUNCHD="$HOME/Library/LaunchAgents"

echo "=== STR Scout Migration: 8753 → 8754 ==="
echo ""

# 1. Find what's serving on port 8753
echo "→ Finding port 8753 server..."
PID_8753=$(lsof -ti tcp:8753 2>/dev/null || true)
if [ -z "$PID_8753" ]; then
    echo "  No process found on 8753 — may already be stopped."
    SERVE_DIR_8753=""
else
    SERVE_DIR_8753=$(lsof -p "$PID_8753" 2>/dev/null | grep cwd | awk '{print $NF}' || true)
    echo "  PID: $PID_8753  |  Directory: $SERVE_DIR_8753"
fi

# 2. Copy HTML files from 8753's directory to STR-Scouts
if [ -n "$SERVE_DIR_8753" ] && [ -d "$SERVE_DIR_8753" ]; then
    echo "→ Copying HTML files from $SERVE_DIR_8753..."
    for f in "$SERVE_DIR_8753"/*.html; do
        [ -f "$f" ] || continue
        fname=$(basename "$f")
        if [ ! -f "$SCOUT_DIR/$fname" ] || [ "$f" -nt "$SCOUT_DIR/$fname" ]; then
            cp "$f" "$SCOUT_DIR/$fname"
            echo "   Copied: $fname"
        else
            echo "   Already current: $fname"
        fi
    done
else
    echo "  Skipping file copy (no 8753 directory found — locate and copy manually if needed)."
fi

# 3. Stop the 8753 server process
if [ -n "$PID_8753" ]; then
    echo "→ Stopping port 8753 server (PID $PID_8753)..."
    kill "$PID_8753" 2>/dev/null && echo "   Stopped." || echo "   Already stopped."
fi

# 4. Remove any 8753 LaunchAgent
echo "→ Removing 8753 LaunchAgents..."
for plist in "$LAUNCHD"/*.plist; do
    [ -f "$plist" ] || continue
    if grep -q "8753" "$plist" 2>/dev/null; then
        label=$(defaults read "$plist" Label 2>/dev/null || basename "$plist" .plist)
        launchctl unload "$plist" 2>/dev/null || true
        rm -f "$plist"
        echo "   Removed: $label"
    fi
done

# 5. List everything now in STR-Scouts
echo ""
echo "→ Files now in $SCOUT_DIR:"
ls -lh "$SCOUT_DIR"/*.html 2>/dev/null || echo "   (none found)"

# 6. Confirm 8754 is still up
echo ""
if lsof -ti tcp:8754 &>/dev/null; then
    MAC_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "YOUR-MAC-IP")
    echo "=== DONE ==="
    echo ""
    echo "Hub (all scouts):   http://$MAC_IP:8754/"
    echo "Cocoa Beach:        http://$MAC_IP:8754/cocoa-beach-fl-market-scout.html"
    echo "Mansfield:          http://$MAC_IP:8754/mansfield-tx-market-scout.html"
    echo "Gulf Shores:        http://$MAC_IP:8754/gulf-shores-al-market-scout.html"
    echo ""
    echo "Port 8753 is shut down. Everything runs on 8754 now."
else
    echo "WARNING: Port 8754 server not detected — check com.strscout.server LaunchAgent."
fi
