// Raw tables loaded by main.py. The dataset comes from the `raw_dataset` var
// (workflow_settings.yaml, overridden by BQ_RAW_DATASET in .env).
const rawDataset = dataform.projectConfig.vars.raw_dataset;

[
  { name: "player_gamelog", description: "LeagueGameLog (players): one row per player per game." },
  { name: "team_gamelog", description: "LeagueGameLog (teams): one row per team per game." },
  { name: "players_index", description: "PlayerIndex (historical): player attributes." },
  { name: "teams", description: "Static list of the 30 NBA franchises (nba_api)." },
].forEach(({ name, description }) =>
  declare({ schema: rawDataset, name, description })
);
