import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Governance & Economic Indicators",
    page_icon="📊",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    gov = pd.read_csv("data/italian_governments.csv")
    sectors = pd.read_csv("data/sectoral_shares_oecd.csv")
    gdp_total = pd.read_csv("data/gdp_total.csv")
    gdp_pc = pd.read_csv("data/gdp_per_capita.csv")
    return gov, sectors, gdp_total, gdp_pc

gov_df, sectors_df, gdp_total_df, gdp_pc_df = load_data()

# Title
st.title("📊 Governance & Economic Indicators")
st.markdown("**Italian Political Stability & Economic Analysis (1946-2024)**")

# Sidebar navigation
page = st.sidebar.radio("Navigate", [
    "🏛️ Government Duration",
    "🏭 Industrial Composition",
    "💰 European GDP Trends"
])

# --- PAGE 1: Government Duration ---
if page == "🏛️ Government Duration":
    st.header("Italian Government Stability")
    
    # Calculate Meloni days
    meloni_start = pd.to_datetime("2022-10-22")
    meloni_days = (datetime.now() - meloni_start).days
    berlusconi_max = gov_df[gov_df['leader'] == 'Silvio Berlusconi']['duration_days'].max()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Meloni Days in Office", f"{meloni_days}")
    with col2:
        st.metric("Berlusconi Record", f"{berlusconi_max}")
    with col3:
        days_to_record = berlusconi_max - meloni_days
        st.metric("Days to Beat Record", f"{days_to_record}")
    
    st.subheader("Historical Government Duration")
    
    # Bar chart - government duration
    fig_gov = px.bar(
        gov_df,
        x='duration_days',
        y='leader',
        orientation='h',
        title='Italian Governments Duration (1946-2024)',
        labels={'duration_days': 'Duration (days)', 'leader': 'Prime Minister'},
        color='duration_days',
        color_continuous_scale='Greys'
    )
    fig_gov.update_layout(
        height=800,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig_gov, use_container_width=True)
    
    st.info("**Note**: Data includes all governments from 1946 to 2024. Giorgia Meloni's current government updates daily.")

# --- PAGE 2: Industrial Composition ---
elif page == "🏭 Industrial Composition":
    st.header("Structural Transformation of Italian Economy")
    st.markdown("**OECD Data (1985-2024)**")
    
    # Line chart - sectoral evolution
    fig_sectors = px.line(
        sectors_df,
        x='year',
        y='share_percent',
        color='sector',
        title='Sectoral Share of Total Economy (%)',
        labels={'year': 'Year', 'share_percent': 'Share (%)', 'sector': 'Sector'},
        markers=True
    )
    fig_sectors.update_layout(height=500)
    st.plotly_chart(fig_sectors, use_container_width=True)
    
    # Pie chart - 2024 composition
    sectors_2024 = sectors_df[sectors_df['year'] == 2024]
    fig_pie = px.pie(
        sectors_2024,
        values='share_percent',
        names='sector',
        title='Sectoral Composition 2024'
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("""
    **Key Insights**:
    - **Manufacturing**: Declined from 56.4% (1985) to 39.4% (2024)
    - **Professional Services**: Emerged from 0% to 16.7% (since 1992)
    - **Tourism**: Stable at ~22-23% (economic pillar)
    - **ICT**: Constant at ~8% throughout the period
    """)

# --- PAGE 3: European GDP Trends ---
elif page == "💰 European GDP Trends":
    st.header("European GDP Comparison")
    
    tab1, tab2 = st.tabs(["GDP Total", "GDP Per Capita"])
    
    with tab1:
        st.subheader("GDP Total - Major European Economies (1975-2024)")
        fig_gdp = px.line(
            gdp_total_df,
            x='year',
            y='gdp_billion_usd',
            color='country_name',
            title='GDP in Billion USD',
            labels={'year': 'Year', 'gdp_billion_usd': 'GDP (Billion USD)', 'country_name': 'Country'},
            markers=True
        )
        fig_gdp.update_layout(height=500)
        st.plotly_chart(fig_gdp, use_container_width=True)
    
    with tab2:
        st.subheader("GDP Per Capita - European Economies (1975-2024)")
        fig_gdp_pc = px.line(
            gdp_pc_df,
            x='year',
            y='gdp_per_capita_usd',
            color='country_name',
            title='GDP Per Capita in USD',
            labels={'year': 'Year', 'gdp_per_capita_usd': 'GDP Per Capita (USD)', 'country_name': 'Country'},
            markers=True
        )
        fig_gdp_pc.update_layout(height=500)
        st.plotly_chart(fig_gdp_pc, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Data Sources**: OECD STAN Database, World Bank, Italian Government Records")
st.markdown("Dashboard by Cristiano Mombello | [LinkedIn Profile](#)")
