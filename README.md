# MLB Baseball Analytics Dashboard 2024

![2024 MLB WAR Leaderboard - Dashboard Preview](https://quickchart.io/chart?c={type:'horizontalBar',data:{labels:['Aaron%20Judge','Bobby%20Witt%20Jr.','Shohei%20Ohtani','Juan%20Soto','Gunnar%20Henderson','Francisco%20Lindor','Elly%20De%20La%20Cruz','Jose%20Ramirez','Ketel%20Marte','Chris%20Sale','Tarik%20Skubal','Zack%20Wheeler'],datasets:[{label:'WAR%202024',data:[11.3,10.5,8.9,8.3,7.9,7.7,6.8,6.5,6.3,6.4,6.0,5.4],backgroundColor:['%2300CC96','%2300CC96','%2300CC96','%2300CC96','%2300CC96','%2300CC96','%2300CC96','%2300CC96','%2300CC96','%23636EFA','%23636EFA','%23636EFA']}]},options:{plugins:{title:{display:true,text:'2024%20MLB%20WAR%20Leaders'}},scales:{xAxes:[{ticks:{beginAtZero:true}}]}}}&backgroundColor=%23111111&width=800&height=500)

A full-stack sabermetrics analytics pipeline built in Python that pulls live 2024 MLB data from FanGraphs via pybaseball, processes it into structured DataFrames, and renders **13 interactive Plotly visualizations** across pitcher, hitter, and team-level dashboards.

---

## What's Inside

### Pitcher Dashboard
| Chart | Description |
|---|---|
| ERA vs FIP vs xFIP | Grouped bar comparing actual vs expected ERA for top 30 starters by WAR |
| K vs BB Scatter | Stuff quality quadrant (bubble size = IP, color = ERA) |
| Pitcher WAR Leaderboard | Horizontal bar chart of top 30 starters |

### Hitter Dashboard
| Chart | Description |
|---|---|
| wRC+ Leaderboard | Top 40 hitters by WAR with league average reference line |
| OBP vs SLG Scatter | 4-quadrant hitter profile (bubble size = WAR, color = wRC+) |
| Plate Discipline | BB% vs K% scatter (bubble size = PA, color = wOBA) |
| Sabermetrics Table | AVG, OBP, SLG, OPS, wOBA, wRC+, HR, RBI, WAR |

### Team Dashboard
| Chart | Description |
|---|---|
| Runs Scored | All 30 teams colored by wRC+ |
| Offense vs Defense | OPS vs ERA scatter for every team |
| ERA vs FIP vs xFIP | Team-level pitching luck indicator |
| Full Team Summary Table | R, HR, OPS, wRC+, ERA, FIP, WHIP, P-WAR |

### WAR Comparison Module
- Side-by-side top 15 hitters vs pitchers by WAR
- Combined top 30 WAR leaderboard (hitters + pitchers)
- CSV export of all three datasets

---

## Key Findings 2024 Season

**Hitters**
- Aaron Judge led all MLB position players with 11.3 WAR
- Bobby Witt Jr. (10.5 WAR) emerged as a true five-tool superstar for Kansas City
- Juan Soto posted a .419 OBP, among the best at reaching base in the modern era

**Pitchers**
- Chris Sale posted the best ERA-FIP gap of any qualified starter (2.38 ERA / 2.09 FIP) — genuinely elite, not lucky
- Paul Skenes debuted at 1.96 ERA in 133 IP — one of the best rookie pitching seasons in recent memory
- Reynaldo Lopez showed a significant ERA-FIP gap (1.99 ERA / 2.92 FIP) — a strong regression candidate heading into 2025

**Teams**
- The Dodgers and Yankees led the league in both offensive output and overall talent concentration
- Several teams with low ERAs had FIPs suggesting unsustainably lucky pitching performances — a useful front office signal

---

## Tech Stack

| Tool | Purpose |
|---|---|
| pybaseball | FanGraphs / Baseball Reference data ingestion |
| pandas | Data cleaning, filtering, and aggregation |
| plotly | Interactive charts and data tables |
| numpy | Numerical operations |
| Python 3.10 | Runtime |

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/jordantaylorkurzweil-hash/mlb-analytics-dashboard-2024.git
cd mlb-analytics-dashboard-2024
```

### 2. Install dependencies
```bash
pip install pybaseball plotly pandas numpy scipy
```

### 3. Run the notebook
Open `BaseballAnalyticsDashboard.ipynb` in Jupyter or Google Colab and run all cells top to bottom.

> Note: pybaseball caching is enabled by default. First run may take 30-60 seconds to pull data. Subsequent runs are fast.

---

## Exported Data

Running Cell 6 exports three CSVs to your working directory:

| File | Contents |
|---|---|
| `2024_hitter_sabermetrics.csv` | Top 40 hitters by WAR with full slash line and advanced metrics |
| `2024_pitcher_sabermetrics.csv` | Top 30 starters by WAR with ERA, FIP, xFIP, K%, BB%, WHIP |
| `2024_team_analytics.csv` | All 30 teams offense + pitching merged |

---

## Metrics Reference

| Metric | Definition |
|---|---|
| WAR | Wins Above Replacement — overall player value |
| wRC+ | Weighted Runs Created Plus — offense relative to league (100 = avg) |
| wOBA | Weighted On-Base Average — run value of each offensive event |
| FIP | Fielding Independent Pitching — ERA based only on K, BB, HR |
| xFIP | Expected FIP — normalizes HR rate to league average |
| ISO | Isolated Power (SLG minus AVG) |
| BABIP | Batting Average on Balls in Play — luck indicator |

---

## Project Structure

```
baseball-analytics-dashboard/
├── BaseballAnalyticsDashboard.ipynb  # Main notebook (all 6 cells)
├── README.md                          # This file
├── preview.png                        # Dashboard preview image
├── 2024_hitter_sabermetrics.csv       # Exported after running Cell 6
├── 2024_pitcher_sabermetrics.csv      # Exported after running Cell 6
└── 2024_team_analytics.csv            # Exported after running Cell 6
```

---

Built as part of an ongoing baseball analytics portfolio. Additional projects include pitch quality modeling using Statcast data — Stuff+ model built with `HistGradientBoostingRegressor` on pybaseball Statcast pulls.

**Skills demonstrated:** Python · pandas · plotly · pybaseball · sabermetrics · data visualization · sports analytics

---

*Data sourced from FanGraphs via pybaseball. All stats reflect the 2024 MLB regular season.*
