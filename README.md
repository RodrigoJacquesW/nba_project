# 🏀 NBA Analytics Data Pipeline & BI Dashboard

End-to-end Data Engineering and Analytics project built using official NBA data, covering the full data lifecycle from raw extraction to business-ready insights.

Extraction → Storage → Modeling → Visualization

The goal of this project is to create a reliable analytical foundation to analyze players, teams, and season performance, delivering interactive and insight-driven dashboards in Power BI.

## Architecture Overview

NBA Stats API  
↓  
Python (Extraction)  
↓  
Google BigQuery (Storage)  
↓  
Dataform (Transformation & Modeling)  
↓  
Power BI (Analytics & Visualization)

## Tech Stack

Data Engineering  
- Python  
- nba_api  
- Google BigQuery  
- Dataform  
- Git / GitHub  

BI & Analytics  
- Power BI  
- Star schema modeling  
- Advanced DAX (benchmarks, league averages, dynamic targets)

## Data Extraction

Data is extracted directly from the NBA Stats API, including both player-level and team-level information.

Endpoints used  
- LeagueGameLog  
- PlayerGameLog  
- LeagueGameLog (Teams)  
- PlayerIndex  
- Teams (Static)

Official player and team headshots are also downloaded and stored to enhance dashboard visuals.

-source : https://github.com/swar/nba_api

## Local Pipeline Orchestration

The entire pipeline is orchestrated through a centralized main() function, allowing end-to-end execution with a single command.

The pipeline performs:
- Player extraction
- Player index extraction
- Team extraction
- Game list extraction
- Player game logs extraction
- Team game logs extraction
- Player and team headshots download
- Execution of all Dataform models

This approach ensures reproducibility, easy testing, and fast iteration.

## Data Modeling

Transformations are handled using Dataform, following a layered modeling approach:

- source: raw BigQuery tables  
- stg: cleaned and standardized data  
- int: intermediate transformations  
- mart: analytical fact and dimension tables  

Core analytical tables  
- fct_player_gamelog  
- fct_teamlog  
- fct_games_unique  
- dim_player  
- dim_team  
- dim_calendar  

The model is optimized for BI performance and analytical accuracy, avoiding common biases such as statistics limited to home games only.

## Business Intelligence

Dashboards were built in Power BI with a strong focus on comparison, context, and performance trends.

Players Dashboard  
- Points, assists, and efficiency metrics  
- Comparison against league averages  
- Scatter plots with highlighted selected player  
- Context-aware benchmarks  

Teams Dashboard  
- Win percentage and season performance  
- Offensive and defensive metrics  
- League average comparisons  
- Dynamic Playoff / Play-In status gauge  

BI Highlights  
- Dynamic benchmarks  
- Context-aware league averages  
- Date-driven analysis using a calendar dimension  
- Clear separation between absolute metrics and relative performance  

## Future Improvements

This project was designed with an analytical and educational focus, but it can be easily extended into a production-grade pipeline:

- Apache Airflow orchestration  
- DAG-based scheduling  
- Incremental data loads  
- Data quality tests  
- CI/CD for Dataform  
- Fully managed cloud deployment  

These features were intentionally not implemented to avoid overengineering, while keeping the architecture ready for scalability.

## Repository Structure

extract/  
├── get_players.py  
├── get_gamelogs.py  
├── get_teamlog.py  
└── ...  

dataform/  
├── source/  
├── stg/  
├── int/  
└── mart/  

images/  
├── players/  
└── teams/  

main.py  
README.md  

## Author

Rodrigo Wolff  
Data Engineering · Analytics Engineering · Business Intelligence

## Final Notes

This project demonstrates more than dashboard creation. It showcases solid data modeling, architectural decision-making, analytical thinking, scalability awareness, and a production-ready mindset.
