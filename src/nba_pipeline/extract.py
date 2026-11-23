"""Extraction from the NBA Stats API (via nba_api).

Each function returns a DataFrame for one season. Column names are kept exactly as
the API returns them: renaming and typing happen in the Dataform staging layer.
"""

import pandas as pd
from nba_api.stats.endpoints import leaguegamelog, playerindex
from nba_api.stats.static import teams

TIMEOUT = 60
SEASON_TYPE = "Regular Season"


def player_gamelog(season: str) -> pd.DataFrame:
    """One row per player per game. A single request returns the whole league."""
    return leaguegamelog.LeagueGameLog(
        season=season,
        season_type_all_star=SEASON_TYPE,
        player_or_team_abbreviation="P",
        timeout=TIMEOUT,
    ).get_data_frames()[0]


def team_gamelog(season: str) -> pd.DataFrame:
    """One row per team per game (two rows per game)."""
    return leaguegamelog.LeagueGameLog(
        season=season,
        season_type_all_star=SEASON_TYPE,
        player_or_team_abbreviation="T",
        timeout=TIMEOUT,
    ).get_data_frames()[0]


def players_index(season: str) -> pd.DataFrame:
    """Player attributes (position, height, draft...).

    `historical_nullable="1"` is required: without it, the endpoint only returns players
    still on a roster today, which drops most of the players of a past season.
    """
    df = playerindex.PlayerIndex(
        season=season,
        league_id="00",
        historical_nullable="1",
        timeout=TIMEOUT,
    ).get_data_frames()[0]
    return df


def teams_static() -> pd.DataFrame:
    """The 30 franchises (static data shipped with nba_api)."""
    return pd.DataFrame(teams.get_teams()).sort_values("full_name").reset_index(drop=True)
