"""Download player headshots and team logos from the NBA CDN.

The Power BI report reads these images from this repository on GitHub, so the output
folders must stay at data/headshots/ (players) and data/headshots/teamsheadshot/ (teams).
"""

from pathlib import Path
from typing import Iterable

import requests

from .config import ROOT_DIR

PLAYERS_DIR = ROOT_DIR / "data" / "headshots"
TEAMS_DIR = PLAYERS_DIR / "teamsheadshot"

PLAYER_URL = "https://cdn.nba.com/headshots/nba/latest/260x190/{id}.png"
TEAM_URL = "https://cdn.nba.com/logos/nba/{id}/{variant}"
TEAM_VARIANTS = ["global/L/logo.png", "primary/L/logo.png", "global/L/logo.svg", "primary/L/logo.svg"]


def download_player_headshots(player_ids: Iterable[int], overwrite: bool = False) -> None:
    PLAYERS_DIR.mkdir(parents=True, exist_ok=True)
    missing = 0
    for pid in player_ids:
        path = PLAYERS_DIR / f"{pid}.png"
        if path.exists() and not overwrite:
            continue
        r = requests.get(PLAYER_URL.format(id=pid), timeout=30)
        if r.ok:
            path.write_bytes(r.content)
        else:
            missing += 1
    print(f"  player headshots in {PLAYERS_DIR.relative_to(ROOT_DIR)} ({missing} not found on CDN)")


def download_team_logos(team_ids: Iterable[int], overwrite: bool = False) -> None:
    TEAMS_DIR.mkdir(parents=True, exist_ok=True)
    for tid in team_ids:
        path = TEAMS_DIR / f"{tid}.png"
        if path.exists() and not overwrite:
            continue
        for variant in TEAM_VARIANTS:
            r = requests.get(TEAM_URL.format(id=tid, variant=variant), timeout=30)
            if not r.ok:
                continue
            if variant.endswith(".png"):
                path.write_bytes(r.content)
            else:
                import cairosvg  # only needed when the CDN has no PNG version

                cairosvg.svg2png(bytestring=r.content, write_to=str(path))
            break
        else:
            print(f"  no logo found for team {tid}")
    print(f"  team logos in {TEAMS_DIR.relative_to(ROOT_DIR)}")
