# Governance & Economic Indicators Dashboard

Interactive Streamlit dashboard analyzing Italian political stability and economic trends.

## 🚀 Live Demo
[View Dashboard](https://your-app.streamlit.app) _(coming soon)_

## 📊 Features
- **Government Duration Analysis**: Historical Italian government stability (1946-2024)
- **Industrial Composition**: OECD sectoral transformation (1985-2024)
- **European GDP Trends**: Comparative analysis of major European economies

## 🛠️ Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Steps

1. **Create GitHub Repository**
   ```bash
   # In this folder, run:
   git init
   git add .
   git commit -m "Initial commit: Governance Dashboard"
   ```

2. **Push to GitHub**
   - Create a new repository on GitHub (e.g., `governance-dashboard`)
   - Run:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/governance-dashboard.git
   git branch -M main
   git push -u origin main
   ```

3. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repo
   - Set main file: `app.py`
   - Click "Deploy"

4. **Get Your Public URL**
   - After deployment, copy the URL (format: `https://your-app.streamlit.app`)
   - Share on LinkedIn!

## 📁 Structure
```
streamlit-governance-dashboard/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── data/                     # CSV data files
│   ├── italian_governments.csv
│   ├── sectoral_shares_oecd.csv
│   ├── gdp_total.csv
│   └── gdp_per_capita.csv
└── README.md
```

## 📝 Data Sources
- **OECD STAN Database**: Industrial composition data
- **World Bank**: GDP statistics
- **Italian Government Records**: Political stability metrics

## 👤 Author
**Cristiano Mombello**
- LinkedIn: [Your Profile](#)

## 📄 License
Data is publicly available. Dashboard code is MIT licensed.
