# 📊 Geopolitical Landscape - Data Analytics Portfolio

> **Interactive data dashboards analyzing Italian political stability, European economic trends, and industrial transformation**

[![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=Databricks&logoColor=white)](https://www.databricks.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)

---

## 🚀 Live Dashboards

### 🏛️ [Governance & Economic Indicators Dashboard](https://dbc-dae8232b-70b7.cloud.databricks.com/sql/dashboards/01f1803cd8b216009e6e19ecc12df942)

**Interactive Databricks AI/BI Dashboard** featuring:

- **Italian Government Duration Analysis** (1946-2024)
  - Historical government stability metrics
  - Prime Minister tenure comparison
  - Real-time Meloni government tracking
  
- **World Leaders Mandate Comparison**
  - 48+ world leaders tracked
  - Dynamic filters for custom analysis
  - Days remaining calculations

- **European GDP Trends** (1975-2024)
  - 6 major European economies
  - Total GDP & Per Capita analysis
  - Historical trend visualization

- **Industrial Composition Evolution** (1985-2024)
  - OECD sectoral data analysis
  - Manufacturing vs Services transformation
  - Tourism sector tracking

**[→ View Live Dashboard](https://dbc-dae8232b-70b7.cloud.databricks.com/sql/dashboards/01f1803cd8b216009e6e19ecc12df942)**

---

## 🌐 Streamlit Web Application

Interactive multi-page dashboard with responsive design:

📂 **[View Streamlit App Code](./streamlit-governance-dashboard/)**

**Features:**
- Government Stability Metrics
- Industrial Composition Charts  
- European GDP Comparison
- Interactive filters and dynamic visualizations

**Ready for deployment** on [Streamlit Cloud](https://share.streamlit.io)

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Data Platform** | Databricks, Unity Catalog, Delta Lake |
| **Data Processing** | Apache Spark, PySpark, Spark SQL |
| **Visualization** | Databricks Dashboards, Streamlit, Plotly |
| **Data Sources** | OECD STAN Database, World Bank API, Italian Government Records |
| **Version Control** | Git, GitHub |

---

## 📁 Project Structure

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

## 📊 Key Insights

### Italian Political Stability
- Analysis of **78 years** of government history (1946-2024)
- Average government duration significantly shorter than EU peers
- Current Meloni government tracking vs historical benchmarks

### Economic Transformation
- **Manufacturing decline**: 56.4% → 39.4% (-17pp, 1985-2024)
- **Professional Services emergence**: 0% → 16.7% (since 1992)
- **Tourism stability**: ~22-23% throughout the period

### European GDP Analysis
- 50-year GDP trends for major economies
- Post-2008 divergence patterns
- Per capita comparison across 6 countries

---

## 📝 Data Sources

- **[OECD STAN Database](https://data-explorer.oecd.org/)** - Industrial composition and sectoral analysis
- **[World Bank Open Data](https://data.worldbank.org/)** - GDP indicators and economic metrics
- **Italian Government Official Records** - Political stability data

---

## 👤 Author

**Cristiano Mombello**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/cristiano-mombello)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/igithub14)

---

## 📄 License

Data is publicly available from official sources. Dashboard code is available under MIT License.

---

<div align="center">
  
**[📊 View Live Dashboard](https://dbc-dae8232b-70b7.cloud.databricks.com/sql/dashboards/01f1803cd8b216009e6e19ecc12df942)** • 
**[💻 Explore Code](./streamlit-governance-dashboard/)** • 
**[🔗 Connect on LinkedIn](https://www.linkedin.com/in/cristiano-mombello)**

</div>
