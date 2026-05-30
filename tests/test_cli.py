"""Tests for DailyVibe."""
from typer.testing import CliRunner
from daily_vibe.cli import app

runner = CliRunner()

def test_help():
    r = runner.invoke(app, ["--help"])
    assert r.exit_code == 0
    assert "DailyVibe" in r.output

def test_stats_no_data():
    r = runner.invoke(app, ["stats"])
    assert r.exit_code == 0
