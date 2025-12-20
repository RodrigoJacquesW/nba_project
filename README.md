# 🏀 NBA Analytics Data Pipeline & BI Dashboard

End-to-end **Data Engineering and Analytics** project built using official NBA data.  
The project covers the complete data lifecycle:

**Extraction → Storage → Modeling → Visualization**

The main goal is to create a reliable analytical foundation to analyze **players, teams, and season performance**, delivering interactive and insight-driven dashboards in Power BI.

---

## 🔍 Architecture Overview

The project follows a modern analytics architecture:

NBA Stats API
↓
Python (Extraction)
↓
Google BigQuery (Storage)
↓
Dataform (Transformation & Modeling)
↓
Power BI (Analytics & Visualization)

yaml
Copiar código

---

## 🛠️ Tech Stack

### Data Engineering
- **Python**
- **nba_api**
- **Google BigQuery**
- **Dataform**
- **Git / GitHub**

### BI & Analytics
- **Power BI**
- Star schema modeling
- Advanced DAX (benchmarks, league averages, dynamic targets)

---

## 📥 Data Extraction

Data is extracted directly from the **NBA Stats API**, including both player-level and team-level information.

### Endpoints used
- `LeagueGameLog`
- `PlayerGameLog`
- `LeagueGameLog (Teams)`
- `PlayerIndex`
- `Teams (Static)`

```python
from nba_api.stats.endpoints import LeagueGameLog
from nba_api.stats.endpoints import PlayerGameLog
from nba_api.stats.endpoints import PlayerIndex
from nba_api.stats.static import teams
Additionally, official headshots for players and teams are downloaded and stored to enhance dashboard visuals.

⚙️ Local Pipeline Orchestration
A centralized main() function orchestrates the entire pipeline execution:

python
Copiar código
def main():
    full_get_player()
    full_get_player_index()
    full_get_teams()
    full_load_games()
    full_get_gamelog()
    full_team_gamelog()
    download_all_headshots()
    download_all_team_logos()
    subprocess.run(["dataform", "run"], check=True)
This approach provides
One-command end-to-end execution

Reproducibility

Easy testing and iteration

🧱 Data Modeling (Transform)
Transformations are handled using Dataform, organized into layered models:

source → raw BigQuery tables

stg → cleaned and standardized data

int → intermediate transformations

mart → analytical fact and dimension tables

Core analytical tables
fct_player_gamelog

fct_teamlog

fct_games_unique

dim_player

dim_team

dim_calendar

The model is optimized for BI performance and analytical accuracy, avoiding common biases (e.g. statistics limited to home games only).

📊 Business Intelligence (Power BI)
Dashboards were built focusing on both players and teams, emphasizing comparison, context, and performance trends.

Players Dashboard
Points, assists, and efficiency metrics

Comparison against league averages

Scatter plots with highlighted selected player

Context-aware benchmarks

Teams Dashboard
Win percentage and season performance

Offensive and defensive metrics

League average comparisons

Dynamic Playoff / Play-In Status Gauge

BI Highlights
Dynamic benchmarks

Context-aware league averages

Date-driven analysis using a calendar dimension

Clear separation between absolute metrics and relative performance

🚀 Future Improvements
This project was designed with an analytical and educational focus, but it can be easily extended into a production-grade pipeline:

🔄 Orchestration with Apache Airflow

⏰ DAG-based scheduling

🔁 Incremental data loads

🧪 Data quality tests

📦 CI/CD for Dataform

☁️ Fully managed cloud deployment

These features were intentionally not implemented to avoid overengineering, while keeping the architecture ready for scalability.

📂 Repository Structure
css
Copiar código
├── extract/
│   ├── get_players.py
│   ├── get_gamelogs.py
│   ├── get_teamlog.py
│   └── ...
├── dataform/
│   ├── source/
│   ├── stg/
│   ├── int/
│   └── mart/
├── images/
│   ├── players/
│   └── teams/
├── main.py
└── README.md
👤 Author
Developed by Rodrigo Wolff
Focused on Data Engineering, Analytics Engineering, and Business Intelligence.
