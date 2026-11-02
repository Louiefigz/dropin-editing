#!/bin/bash
# Puts the kit's Python (made by ./setup.sh) first on PATH for every command Claude Code runs here.
# Added even before setup has run, so it takes effect as soon as setup creates the folder.
VENV="$CLAUDE_PROJECT_DIR/plugins/dropin-ai-editor/.venv/bin"
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo "export PATH=\"$VENV:\$PATH\"" >> "$CLAUDE_ENV_FILE"
fi
exit 0
