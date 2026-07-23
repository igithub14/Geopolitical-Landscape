# Geopolitical Landscape - Data Analytics Portfolio

Interactive data dashboards analyzing Italian political stability, European economic trends, and industrial transformation.

[![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=Databricks&logoColor=white)](https://www.databricks.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Vega-Lite](https://img.shields.io/badge/Vega--Lite-5-F46D43?style=for-the-badge)](https://vega.github.io/vega-lite/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)

---

## Dashboards

### 1. Governance & Economic Indicators
[View Dashboard](https://dbc-dae8232b-70b7.cloud.databricks.com/sql/dashboards/01f1803cd8b216009e6e19ecc12df942)

Comprehensive multi-page dashboard covering 78 years of Italian political history, European economic trends, and industrial transformation. Five main analytical sections:

#### Section 1: Italian Government Stability (1946-2024)
Historical timeline of Italian government durations with custom Vega visualization. Features real-time Meloni government counter tracking progress toward Berlusconi's record (1,801 days), dynamic leader search with aggregated tenure metrics, and data quality annotations distinguishing verified vs. estimated periods.

#### Section 2: Political Power Structure & Networks
Interactive hierarchical visualization of Italian institutional architecture using custom Vega-Lite specifications. Organizational chart of constitutional bodies (President, Parliament, Government) with institutional dependencies and separation of powers.

#### Section 3: European GDP Trends (1975-2024)
50-year comparative analysis of 6 major European economies (Germany, UK, France, Italy, Spain, Netherlands). Dual visualization: absolute GDP trends highlighting post-2008 divergence patterns, and per capita growth comparison revealing productivity differentials. Data from World Bank API with Eurostat volume index validation.

#### Section 4: Industrial Composition & Evolution (1985-2024)
Structural transformation analysis from OECD STAN Database showing Manufacturing decline (56.4% → 39.4%, -17pp), Professional Services emergence (0% → 16.7% since 1992), and Tourism stability (21-23%). Line chart with 5 macro-sectors tracking 40 years of economic reallocation, complemented by 2024 snapshot pie chart.

#### Section 5: Diplomatic Presence & Missions
Analysis of Italian diplomatic network and international relations. Mapping of embassy presence, consular missions, and multilateral organization participation. Section under active development.

---

## Streamlit Application

[View Code](./streamlit-governance-dashboard/)

Multi-page dashboard with government stability metrics, industrial composition charts, European GDP comparison, and dynamic visualizations. Ready for deployment on [Streamlit Cloud](https://share.streamlit.io).

---

## Technology Stack

| Category | Technologies |
|----------|-------------|
| Data Platform | Databricks, Unity Catalog, Delta Lake |
| Data Processing | Apache Spark, PySpark, Spark SQL |
| Visualization | Databricks Dashboards, Vega-Lite, Streamlit, Plotly |
| Data Sources | OECD STAN Database, World Bank API, Italian Government Records |
| Version Control | Git, GitHub |

---

## Project Structure

```
Geopolitical-Landscape/
├── README.md                                    # Project documentation
├── LICENSE                                      # Apache 2.0 License
├── .gitignore                                   # Git ignore rules
│
├── dashboards/                                  # Databricks Dashboards (published)
│   ├── Governance & Economic Indicators         # ID: 01f1803cd8b216009e6e19ecc12df942
│   │   ├── Section 1: Government Stability      # Italian cabinets 1946-2024
│   │   ├── Section 2: Political Networks        # Institutional hierarchy (Vega-Lite)
│   │   ├── Section 3: European GDP Trends       # 6 economies, 50 years
│   │   ├── Section 4: Industrial Composition    # OECD sectoral data
│   │   └── Section 5: Diplomatic Presence       # Under development
│   └── (Additional dashboards...)               
│
├── notebooks/                                   # ETL & Analysis Notebooks
│   ├── World_Bank_GDP_Data_Loader.py            # GDP data ingestion (World Bank API)
│   ├── Eurostat_GDP_Volume_Loader.ipynb         # GDP volume indices (Eurostat API)
│   ├── GovernmentDurationMetrics.ipynb          # Italian government duration analysis
│   └── Political_Network_Data_Loader.ipynb      # Political network relationships data
│
├── automation/                                  # Scheduled Automation Scripts
│   ├── git_daily_safety_backup.py               # Daily safety backup (23:00 Europe/Rome)
│   │                                            # - Auto-commit all changes with timestamp
│   │                                            # - Push to GitHub (main branch)
│   │                                            # - Email notifications (success/failure)
│   │                                            # - Runs as Databricks Job
│   └── BACKUP_SETUP_INSTRUCTIONS.md             # Complete setup guide for backup job
│
├── unity_catalog/                               # Data Catalog Tables
│   └── geopolitics_data_catalog.processed/      # Processed/curated layer
│       ├── italian_government_duration          # Government stability metrics
│       ├── world_gdp_total                      # GDP absolute values
│       ├── world_gdp_per_capita                 # GDP per capita
│       ├── sectoral_shares_oecd                 # Industrial composition
│       └── (Additional tables...)              
│
└── streamlit-governance-dashboard/              # Streamlit Web Application
    ├── app.py                                   # Main Streamlit app
    ├── requirements.txt                         # Python dependencies
    ├── README.md                                # App documentation
    └── data/                                    # Local CSV datasets (for deployment)
        ├── italian_governments.csv
        ├── sectoral_shares_oecd.csv
        ├── gdp_total.csv
        └── gdp_per_capita.csv
```

**Architecture Notes**:
* **ETL Flow**: Notebooks → Unity Catalog → Databricks Dashboards
* **Data Lineage**: External APIs (World Bank, Eurostat, OECD) → Bronze (raw) → Processed (curated) → Dashboard Datasets
* **Streamlit App**: Standalone deployment using exported CSV snapshots for portability
* **Dashboard Credentials**: Individual data permissions (row-level security enabled)

---

## 🛡️ Automated Backup System

**Daily Safety Backup** - Automated Git commit and push at 23:00 (Europe/Rome)

### Features
* **Automated Commit**: All changes committed daily with timestamped message
* **GitHub Push**: Automatic push to remote repository
* **Email Notifications**: Success/failure reports sent to cristiano.mombello@gmail.com
* **Error Handling**: Comprehensive error detection and reporting
* **Disaster Recovery**: Ensures all work backed up daily to GitHub

### Schedule
* **Frequency**: Daily
* **Time**: 23:00 (11:00 PM) Europe/Rome timezone
* **Script**: `git_daily_safety_backup.py`
* **Execution**: Databricks Job (automated)

### Monitoring
* Email notifications for every run (success or failure)
* Job run history in Databricks Workflows
* GitHub commit log: [View Commits](https://github.com/igithub14/Geopolitical-Landscape/commits/main)

**Benefits**:
* Zero data loss risk - maximum 24h recovery window
* Automated safety net for all project work
* Peace of mind for continuous development

---

## Key Insights

**Italian Political Stability**: 78 years of government history (1946-2024). Average duration significantly shorter than EU peers. Current Meloni government tracked against historical benchmarks.

**Economic Transformation**: Manufacturing decline from 56.4% to 39.4% (-17pp, 1985-2024). Professional Services emergence from 0% to 16.7% (since 1992). Tourism stability at 22-23% throughout period.

**European GDP**: 50-year trends for major economies. Post-2008 divergence patterns. Per capita comparison across 6 countries.

---

## Data Sources

[OECD STAN Database](https://data-explorer.oecd.org/) - Industrial composition and sectoral analysis  
[World Bank Open Data](https://data.worldbank.org/) - GDP indicators and economic metrics  
Italian Government Official Records - Political stability data

---

## Author

**Cristiano Mombello**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/igithub14)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/cristiano-m-47139b36b/)

---

## License

Data is publicly available from official sources. Dashboard code is available under Apache License 2.0.
