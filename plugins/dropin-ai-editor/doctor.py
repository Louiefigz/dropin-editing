#!/usr/bin/env python3
"""DropIn AI Editor — machine check + install planner.

Checks what's already on this machine and prints the EXACT commands to install ONLY
what's missing (check-then-install). Run it, install the gaps it lists, run it again,
repeat until it says READY. Exit 0 = ready, 1 = something to install.
"""
import shutil, subprocess, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"; X = "\033[0m"
def mark(b): return f"{G}OK{X}" if b else f"{R}MISSING{X}"
def has(c): return shutil.which(c) is not None
def pyimp(m):
    try: __import__(m); return True
    except Exception: return False

brew_need, pip_need, notes = [], [], []
crit_ok = True

print("\n  DropIn AI Editor — machine check\n  " + "-" * 36)

# ── system tools ──
ffmpeg, ffprobe = has("ffmpeg"), has("ffprobe")
libass = False
if ffmpeg:
    try:
        out = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True).stdout
        libass = "subtitles" in out
    except Exception:
        pass
print(f"  ffmpeg + libass    {mark(ffmpeg and ffprobe and libass)}")
if not (ffmpeg and ffprobe and libass): brew_need.append("ffmpeg"); crit_ok = False
ytd = has("yt-dlp"); print(f"  yt-dlp (URL in)    {mark(ytd)}")
if not ytd: brew_need.append("yt-dlp"); crit_ok = False
tess = has("tesseract"); print(f"  tesseract (audit)  {mark(tess)}  {Y}(optional){X}")
if not tess: notes.append("optional: brew install tesseract (caption checks)")
rcl = has("rclone"); print(f"  rclone (drive in)  {mark(rcl)}  {Y}(optional){X}")
if not rcl: notes.append("optional: brew install rclone (only for Google Drive footage)")

# ── python deps ──
print("  " + "-" * 36)
deps_missing = False
for mod in ["numpy", "cv2", "PIL", "scipy", "librosa", "soundfile", "requests"]:
    ok = pyimp(mod); print(f"  py:{mod:<15} {mark(ok)}")
    if not ok: deps_missing = True; crit_ok = False
if deps_missing: pip_need.append("-r requirements.txt")

# ── assets ──
print("  " + "-" * 36)
font = any((ROOT / "skills/caption-clips/fonts").glob("*.ttf")) or \
       any((ROOT / "skills/caption-clips/fonts/free_font").glob("*.otf"))
yunet = (ROOT / "skills/horizontal-to-vertical/scripts/yunet.onnx").exists()
print(f"  caption fonts      {mark(font)}")
print(f"  face model (yunet) {mark(yunet)}")
crit_ok &= font and yunet
if not font: notes.append("caption fonts missing — re-download the kit")
if not yunet: notes.append("face model yunet.onnx missing — re-download the kit")

tools_ok = crit_ok

# ── transcription (key-free by default via local whisper) ──
print("  " + "-" * 36)
from dropin_credentials import load_keys
load_keys()
def keyset(name):
    return bool(os.environ.get(name))
aai = keyset("ASSEMBLYAI_API_KEY")
groq = keyset("GROQ_API_KEY")
print(f"  AssemblyAI ingest  {mark(aai)}   {Y}(standard /edit transcription){X}")
print(f"  Gemini listener    {mark(keyset('GEMINI_API_KEY'))}   {Y}(listener notes; missing notes are reported){X}")
print(f"  Groq audit/fallback {mark(groq)}   {Y}(separate from primary AssemblyAI ingest){X}")
crit_ok &= aai
if not aai: notes.append("Open ONBOARDING.md: connect AssemblyAI with onboard.py set ASSEMBLYAI_API_KEY")
print(f"  editorial/style    {mark(True)}   {Y}(active agent; no extra model API key){X}")

# ── verdict + install plan ──
print("  " + "-" * 36)
if crit_ok:
    print(f"  {G}LOCAL TOOLS READY{X} — connections still need their own read checks; run:  /edit <your link>   (or ./bin/dropin-ai-editor \"<link>\")\n")
    sys.exit(0)

if tools_ok:
    print(f"  {G}TOOLS READY{X} — next, connect your keys: open this folder in Claude Code and say")
    print("  \"Set up DropIn AI Editor for me\".")
    for n in notes:
        if n.startswith("optional"):
            print(f"    · {n}")
    print("")
    sys.exit(1)

print(f"  {R}NOT READY{X} — install ONLY what's missing:\n")
if brew_need:
    if not has("brew"):
        print("    # Homebrew first: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
    print(f"    brew install {' '.join(dict.fromkeys(brew_need))}")
if pip_need:
    print(f"    bash setup.sh   (from the kit's folder: {ROOT.parent.parent})")
for n in notes:
    print(f"    ! {n}")
print("\n  Then re-check:  bash setup.sh\n")
sys.exit(1)
