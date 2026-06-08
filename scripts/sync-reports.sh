#!/bin/bash
# Sync latest HTML reports from repo to ~/STR-Scouts serving directory
# Run manually or wire into your Mansfield cron to keep files fresh

SCOUT_DIR="$HOME/STR-Scouts"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[$(date)] Syncing STR Scout reports..."

# Pull latest from repo
git -C "$REPO_DIR" pull --ff-only origin claude/cocoa-beach-market-scout-mxIik 2>&1

# Copy all scout HTMLs
cp "$REPO_DIR/index.html" "$SCOUT_DIR/"
[ -f "$REPO_DIR/cocoa-beach-fl-market-scout.html" ] && cp "$REPO_DIR/cocoa-beach-fl-market-scout.html" "$SCOUT_DIR/"
[ -f "$REPO_DIR/gulf-shores-scout-dashboard.html" ]  && cp "$REPO_DIR/gulf-shores-scout-dashboard.html"  "$SCOUT_DIR/"
[ -f "$REPO_DIR/scout-dashboard.html" ]              && cp "$REPO_DIR/scout-dashboard.html"               "$SCOUT_DIR/"

echo "[$(date)] Sync complete. Serving dir: $SCOUT_DIR"
