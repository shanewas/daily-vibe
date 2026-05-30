"""📓 DailyVibe — Beautiful dev journaling with streaks and joy."""

import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(
    name="dv",
    help="📓 DailyVibe — Your dev journal that actually feels good. Log wins. See streaks. Export beauty.",
    add_completion=False,
    rich_markup_mode="rich",
)

console = Console()

DATA_DIR = Path.home() / ".daily-vibe"
DATA_FILE = DATA_DIR / "entries.json"

VIBE_EMOJIS = {
    "ship": "🚀", "win": "🏆", "learn": "🧠", "grind": "💪",
    "bug": "🐛", "design": "🎨", "idea": "💡", "team": "👥", "chill": "🧘"
}

def load_entries() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text())

def save_entries(entries: list[dict]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(entries, indent=2))

def get_streak(entries: list[dict]) -> int:
    if not entries:
        return 0
    days = sorted({e["date"] for e in entries}, reverse=True)
    streak = 0
    current = date.today()
    for d in days:
        d_date = date.fromisoformat(d)
        if d_date == current:
            streak += 1
            current -= timedelta(days=1)
        elif d_date == current - timedelta(days=1):
            streak += 1
            current -= timedelta(days=1)
        else:
            break
    return streak

@app.command()
def today(
    win: str = typer.Argument(..., help="What did you ship or accomplish today?"),
    mood: int = typer.Option(7, "--mood", "-m", min=1, max=10, help="Mood 1-10"),
    vibe: str = typer.Option("ship", "--vibe", "-v", help="Tag: ship/win/learn/..."),
):
    """✨ Log today's win + mood. Builds your streak automatically."""
    entries = load_entries()
    today_str = date.today().isoformat()
    entries = [e for e in entries if e["date"] != today_str]
    entry = {
        "date": today_str,
        "win": win.strip(),
        "mood": mood,
        "vibe": vibe.lower(),
        "ts": datetime.now().isoformat(),
    }
    entries.append(entry)
    save_entries(entries)
    emoji = VIBE_EMOJIS.get(vibe.lower(), "✨")
    mood_bar = "🔥" * (mood // 2) + "·" * (5 - mood // 2)
    console.print(Panel(
        f"[bold green]{emoji}  {win}[/bold green]\n\n"
        f"[bold]Mood:[/bold] {mood}/10  {mood_bar}\n"
        f"[bold]Vibe:[/bold] {vibe} {emoji}\n"
        f"[bold]Streak:[/bold] {get_streak(entries)} days 🔥",
        title=f"📓 Logged for {today_str}",
        border_style="green",
    ))
    if get_streak(entries) >= 3:
        console.print("[bold orange1]🔥 Nice streak! Keep the momentum going.[/bold orange1]")

@app.command()
def week():
    """📅 Show the last 7 days of wins in a gorgeous table."""
    entries = load_entries()
    if not entries:
        console.print("[yellow]No entries yet. Try: dv today \"shipped the thing\"[/yellow]")
        return
    recent = sorted(entries, key=lambda e: e["date"], reverse=True)[:7]
    streak = get_streak(entries)
    table = Table(title=f"📓 Last 7 Days — Current Streak: {streak} 🔥", show_header=True, header_style="bold cyan")
    table.add_column("Date", style="dim", width=12)
    table.add_column("Win", style="bold")
    table.add_column("Mood", justify="center", width=8)
    table.add_column("Vibe", justify="center", width=10)
    for e in recent:
        mood = e["mood"]
        mood_str = f"{mood}/10 " + ("🔥" if mood >= 8 else "🙂" if mood >= 5 else "😔")
        vibe = e.get("vibe", "ship")
        emoji = VIBE_EMOJIS.get(vibe, "✨")
        table.add_row(
            e["date"],
            e["win"][:55] + ("..." if len(e["win"]) > 55 else ""),
            mood_str,
            f"{emoji} {vibe}",
        )
    console.print(table)
    console.print(f"\n[italic dim]Total entries: {len(entries)} • Data: ~/.daily-vibe/entries.json[/italic dim]")

@app.command()
def export(
    fmt: str = typer.Option("md", "--format", "-f", help="md or json"),
    out: Optional[Path] = typer.Option(None, "--out", "-o", help="Output file path"),
):
    """📤 Export your journal (beautiful Markdown by default)."""
    entries = load_entries()
    if not entries:
        console.print("[yellow]Nothing to export yet.[/yellow]")
        return
    out = out or Path.cwd() / f"daily-vibe-journal.{fmt}"
    if fmt == "json":
        out.write_text(json.dumps(entries, indent=2))
    else:
        lines = ["# 📓 DailyVibe Journal\n", f"_Exported {datetime.now().strftime('%Y-%m-%d')} • {len(entries)} entries_\n"]
        streak = get_streak(entries)
        lines.append(f"**Current streak:** {streak} days 🔥\n")
        by_month: dict[str, list] = {}
        for e in sorted(entries, key=lambda x: x["date"], reverse=True):
            month = e["date"][:7]
            by_month.setdefault(month, []).append(e)
        for month, es in sorted(by_month.items(), reverse=True):
            lines.append(f"\n## {month}\n")
            for e in es:
                emoji = VIBE_EMOJIS.get(e.get("vibe", ""), "✨")
                lines.append(f"- **{e['date']}** {emoji} {e['win']}  — mood {e['mood']}/10\n")
        out.write_text("".join(lines))
    console.print(f"[green]✅ Exported to[/green] [bold]{out}[/bold]")

@app.command()
def stats():
    """📊 Quick stats + longest streak."""
    entries = load_entries()
    if not entries:
        console.print("No data yet.")
        return
    moods = [e["mood"] for e in entries]
    avg = sum(moods) / len(moods)
    best_day = max(entries, key=lambda e: e["mood"])
    console.print(Panel(
        f"Total entries: [bold]{len(entries)}[/bold]\n"
        f"Average mood: [bold]{avg:.1f}/10[/bold]\n"
        f"Current streak: [bold]{get_streak(entries)}[/bold] 🔥\n"
        f"Best day: [bold]{best_day['date']}[/bold] — {best_day['win'][:40]} (mood {best_day['mood']})",
        title="📊 Your Vibe Stats",
        border_style="magenta",
    ))

if __name__ == "__main__":
    app()
