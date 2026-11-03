#!/usr/bin/env bash
# One-command setup for DropIn AI Editor (macOS). Safe to run again: it only adds what's missing.
DIR="$(cd "$(dirname "$0")" && pwd)"
PLUG="$DIR/plugins/dropin-ai-editor"
VENV="$PLUG/.venv"

say()  { printf '\n\033[1m%s\033[0m\n' "$1"; }
ok()   { printf '  \033[92m✓\033[0m %s\n' "$1"; }
warn() { printf '  \033[93m!\033[0m %s\n' "$1"; }
stop() { printf '\n  \033[91m✗ %s\033[0m\n\n' "$1"; exit 1; }

say "DropIn AI Editor setup"

# 1. The basics
[ "$(uname -s)" = "Darwin" ] || stop "This kit runs on macOS for now."
if [ -n "$CLAUDECODE" ] || command -v claude >/dev/null 2>&1; then ok "Claude Code found"
else warn "Claude Code not found. Install it from https://claude.com/claude-code before making clips."; fi
command -v brew >/dev/null 2>&1 || stop "Homebrew is needed first. Install it from https://brew.sh, then run: bash setup.sh"
ok "Homebrew found"

# 2. Video tools
say "Installing video tools (ffmpeg, tesseract, yt-dlp)..."
for tool in ffmpeg tesseract yt-dlp; do
  if brew list --versions "$tool" >/dev/null 2>&1; then ok "$tool already installed"
  else brew install "$tool" >/dev/null && ok "$tool installed" || stop "Could not install $tool. Try: brew install $tool"; fi
done

# 3. Python packages, in a private folder so nothing else on your Mac changes
say "Installing Python packages (a few minutes the first time)..."
PY=""
for candidate in python3.12 python3.13 python3.11 python3.10 python3; do
  if command -v "$candidate" >/dev/null 2>&1 &&
     "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
    PY="$candidate"; break
  fi
done
[ -n "$PY" ] || stop "Python 3.10 or newer is needed. Install it with: brew install python@3.12"
ok "Using $("$PY" --version)"
[ -x "$VENV/bin/python3" ] || "$PY" -m venv "$VENV" || stop "Could not create the Python environment."
"$VENV/bin/python3" -m pip install -q --upgrade pip >/dev/null 2>&1
"$VENV/bin/python3" -m pip install -q -r "$PLUG/requirements.txt" || stop "Python packages did not install. Copy the error above and ask Claude Code to fix it."
ok "Core packages installed"
if "$VENV/bin/python3" -m pip install -q -r "$PLUG/requirements-local.txt" >/dev/null 2>&1; then
  ok "Offline transcription installed (optional)"
else
  warn "Skipped offline transcription (optional; AssemblyAI does the normal transcripts)"
fi

# 4. Health check
say "Checking everything..."
"$VENV/bin/python3" "$PLUG/doctor.py"
echo "  (Missing API keys are expected here. Claude Code connects them in the next step.)"

say "Setup done. Next:"
echo "  1. Open this folder in Claude Code."
echo "  2. Say: Set up DropIn AI Editor for me"
echo "  3. Then give it a video: Make shorts from <your YouTube link>"
echo ""
echo "  When your clips are ready to post, upload them to DropIn (https://getdropin.io)"
echo "  to schedule them to every platform from one dashboard."
echo ""
