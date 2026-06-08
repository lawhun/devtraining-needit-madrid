#!/bin/bash
# DEPRECATED — DO NOT USE
#
# This script was the original attempt to run the Cocoa Beach STR Scout via launchd.
# It failed because `claude --print` cannot access Cowork artifacts, AirROI MCP tools,
# or first-party WebSearch — all required by the daily scout skill.
#
# The correct approach is the Cowork scheduler:
#   Skill: cocoa-beach-str-scout
#   Path:  ~/.claude/skills/cocoa-beach-str-scout/SKILL.md
#   Cron:  30 6 * * * (6:30 AM ET)
#   Setup: mcp__scheduled-tasks__create_scheduled_task
#
# See: skills/cocoa-beach-str-scout/SKILL.md in this repo for the full skill spec.
#
# The companion launchd plist (scripts/com.strscout.cocoa-beach.plist) is also deprecated.

echo "[$(date)] ERROR: This script is deprecated. Use the Cowork scheduler skill instead."
echo "  Skill: cocoa-beach-str-scout"
echo "  Docs:  $(dirname "$0")/../skills/cocoa-beach-str-scout/SKILL.md"
exit 1
