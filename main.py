"""NBA analytics pipeline: NBA Stats API -> BigQuery (raw) -> Dataform (staging, marts).

Usage (from anywhere):
    python main.py                  # extract + load + transform
    python main.py --images         # also refresh player headshots and team logos
    python main.py --skip-dataform  # only extract + load
    python main.py --season 2024-25
"""

import argparse
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from nba_pipeline import extract, images  # noqa: E402
from nba_pipeline.config import get_settings  # noqa: E402
from nba_pipeline.load import load_raw  # noqa: E402
from nba_pipeline.transform import run_dataform  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--season", help="NBA season, e.g. 2025-26 (default: NBA_SEASON or 2025-26)")
    parser.add_argument("--images", action="store_true", help="download missing headshots and logos")
    parser.add_argument("--skip-dataform", action="store_true", help="do not run the Dataform models")
    args = parser.parse_args()

    settings = get_settings()
    if args.season:
        settings = replace(settings, season=args.season)
    print(f"Season {settings.season} -> project {settings.gcp_project_id}")

    print("[1/3] Extract + load raw tables")
    player_logs = extract.player_gamelog(settings.season)
    load_raw(player_logs, "player_gamelog", settings)
    load_raw(extract.team_gamelog(settings.season), "team_gamelog", settings)
    load_raw(extract.players_index(settings.season), "players_index", settings)
    teams = extract.teams_static()
    load_raw(teams, "teams", settings)

    if args.images:
        print("[2/3] Images")
        images.download_player_headshots(sorted(player_logs["PLAYER_ID"].unique()))
        images.download_team_logos(teams["id"])
    else:
        print("[2/3] Images skipped (use --images)")

    if args.skip_dataform:
        print("[3/3] Dataform skipped")
    else:
        print("[3/3] Dataform run")
        run_dataform(settings)

    print("Done.")


if __name__ == "__main__":
    main()
