#!/bin/bash
# Douyin to Text Skill - Shell wrapper for Claude Code

# This script is invoked when user types /dy2text in Claude Code

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null
fi

# Run the skill
python "$SCRIPT_DIR/dy2text.py" "$@"
