# DropIn AI Editor — free starter kit

A free, open-source kit from [DropIn](https://getdropin.io).

**Give it a long video. Get back finished, captioned vertical clips ready to post.**

DropIn AI Editor runs inside Claude Code on your Mac. It finds the best moments in a podcast,
interview or talk, cuts them cleanly, keeps the speaker's face centered in a 9:16 frame, adds
word-by-word captions and music, then checks every clip before handing it over.
The [playbook](DropIn-AI-Editor-Playbook.pdf) walks through how it works.

## What you need
- **A Mac.** Windows isn't supported yet.
- **[Claude Code](https://claude.com/claude-code)**, the desktop app or the terminal version. It does the editing, so
  you don't need any other AI subscription.
- **[Homebrew](https://brew.sh)**, a free installer for Mac tools. If you don't have it, Claude Code will walk you
  through it.
- **Three accounts** you'll connect during setup: [AssemblyAI](https://www.assemblyai.com/dashboard)
  (transcripts, pay as you go), [Google AI Studio](https://aistudio.google.com/apikey) (Gemini) and
  [Groq](https://console.groq.com/keys). Gemini and Groq both have free tiers.

## Get started
1. **Download the kit.** On this page click **Code → Download ZIP** and unzip it. (Or `git clone` it.)
2. **Open the folder in Claude Code.** If it asks whether to trust the folder, say yes.
3. **Say: "Set up DropIn AI Editor for me."** It installs everything (about a minute), then connects
   your three accounts one at a time. You paste each key into a private prompt, never into the chat.
4. **Make clips.** Say **"Make shorts from &lt;your YouTube link&gt;"**, or drop a video file in and say
   "make shorts from this". Finished clips land in the project's `20_DELIVER/` folder.

Prefer the terminal? Run `bash setup.sh` yourself, then start `claude` in this folder. Run it
again any time to check that everything is still working.

## What's INCLUDED — the full method
The complete editorial brain ships here (anonymized): the clip-selection rubric, the cut logic,
the spice caption styling, the audit rules, and the lift patterns. **Out of the box it cuts with
real editorial judgment, not a generic template** — the clips come out to a high bar, and the
active agent applies the editorial references and inspects the result; additional audits are opt-in.

## What YOU supply
| You bring | Where |
|---|---|
| Editing connections (AssemblyAI, Gemini, agent reads bundled editorial docs; optional audit/fallback keys) | Agent-guided [onboarding](ONBOARDING.md); secrets saved privately |
| Footage | the project's `00_SOURCE/` (or a URL / drive link) |
| Music | your royalty-free tracks → `DROPIN_MUSIC=/your/music` |
| Font & brand | swap the bundled free font; set your cover logo / product name |

## What's deliberately NOT in here
Only the things that are pure liability and add nothing to clip quality:
- **API keys** — bring your own; [complete inventory and setup](docs/CONNECTIONS.md).
- **Licensed fonts** — free **Montserrat** ships instead (looks the same, legal to redistribute).
- **Personal / client data** — real names, revenue figures, and client footage were anonymized
  or removed. None of it is used to make a clip.

## First use and connections
The agent walks through [ONBOARDING.md](ONBOARDING.md) before the first production job and saves
progress. **AssemblyAI** is the primary transcription provider, matching the current `/edit`
pipeline. The active agent reads the bundled editorial documents without an Anthropic/OpenAI key.
Gemini and optional audit/fallback credentials have distinct roles in the
[connection inventory](docs/CONNECTIONS.md). Some current team-native integrations are companion
installations; the inventory names those prerequisites rather than treating keys as a full install.

## Deliver to Frame.io + Monday
Say **“push these clips to Frame and Monday.”** First use connects your own accounts and asks
which brands you edit for, your editor initials, and where each brand's clips should go.
Shorts are the default. The kit handles filenames, Frame uploads and linked Monday review cards.
[Delivery setup](plugins/dropin-ai-editor/skills/monday/references/onboarding.md).

## Posting your clips
This kit makes the clips; it doesn't post them. Posting a batch by hand to YouTube, Instagram,
TikTok, LinkedIn and Facebook means dozens of separate uploads. [DropIn](https://getdropin.io)
publishes them all from one calendar, with titles and descriptions for each platform and an
approval step for clients or your team. If you edit for several brands, it also keeps ideas,
raw footage and edits for each one on a shared board. 10-day free trial.
