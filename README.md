# 📓 DailyVibe `dv`

**Your dev journal that actually feels good.**

Log wins. Watch your streak grow. Export gorgeous Markdown for Notion/Obsidian.

<p align="center">
  <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg">
  <a href="https://github.com/shanewas/daily-vibe/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/shanewas/daily-vibe?style=social"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
</p>

## ✨ Why DailyVibe?

Most dev journals die after 3 days. This one feels *good* to use.

- 🔥 Instant beautiful streak counter
- 📊 Mood tracking with color vibes
- 📤 One-command gorgeous Markdown export
- 🪶 Zero config, JSON store in ~/.daily-vibe

## 🚀 Install

```bash
pipx install git+https://github.com/shanewas/daily-vibe.git
```

## 🎯 Usage

```bash
# Log today's win (mood 1-10 optional)
dv today "shipped the new auth flow" --mood 9 --vibe=ship

# See the last week + streak

dv week

# Export to Markdown (ready for Notion/Obsidian)
dv export --format md --out my-journal.md

# Quick stats
dv stats
```

## 🧪 Development

```bash
git clone https://github.com/shanewas/daily-vibe.git
cd daily-vibe
pip install -e .
pytest -q
```

Built with ❤️ in one vibe session by [@shanewas](https://github.com/shanewas).

MIT License
