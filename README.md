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

Comprehensive multi-page dashboard covering 78 years of Italian political history, European economic trends, and industrial transformation. Four main analytical sections:

#### Section 1: Italian Government Stability (1946-2024)
Historical timeline of Italian government durations with custom Vega visualization. Features real-time Meloni government counter tracking progress toward Berlusconi's record (1,801 days), dynamic leader search with aggregated tenure metrics, and data quality annotations distinguishing verified vs. estimated periods.

#### Section 2: Political Power Structure & Networks
Interactive hierarchical visualization of Italian institutional architecture using custom Vega-Lite specifications. Organizational chart of constitutional bodies (President, Parliament, Government) with institutional dependencies and separation of powers.

#### Section 3: European GDP Trends (1975-2024)
50-year comparative analysis of 6 major European economies (Germany, UK, France, Italy, Spain, Netherlands). Dual visualization: absolute GDP trends highlighting post-2008 divergence patterns, and per capita growth comparison revealing productivity differentials. Data from World Bank API with Eurostat volume index validation.

#### Section 4: Industrial Composition & Evolution (1985-2024)
Structural transformation analysis from OECD STAN Database showing Manufacturing decline (56.4% → 39.4%, -17pp), Professional Services emergence (0% → 16.7% since 1992), and Tourism stability (21-23%). Line chart with 5 macro-sectors tracking 40 years of economic reallocation, complemented by 2024 snapshot pie chart.

### 2. Political Power Structure & Networks
[View Dashboard](https://dbc-dae8232b-70b7.cloud.databricks.com/sql/dashboards/01f1841dddfa162f8b1f9931d4b33db7)

Interactive hierarchical visualization of Italian institutional architecture using custom Vega-Lite specifications. Features organizational chart of constitutional bodies (President, Parliament, Government), institutional dependencies with separation of powers, and custom SVG-based node styling. Demonstrates advanced dashboard techniques including recursive hierarchy layout algorithms, dynamic edge rendering, and data-driven positioning logic.

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
├── streamlit-governance-dashboard/    # Streamlit web application
│   ├── app.py                        # Main application
│   ├── data/                         # CSV datasets
│   │   ├── italian_governments.csv
│   │   ├── sectoral_shares_oecd.csv
│   │   ├── gdp_total.csv
│   │   └── gdp_per_capita.csv
│   ├── requirements.txt
│   └── README.md
├── Eurostat_GDP_Volume_Loader.ipynb  # Data ingestion notebook
├── GovernmentDurationMetrics.ipynb   # Analysis notebook
└── World_Bank_GDP_Data_Loader.py     # ETL script
```

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
