# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# DBTITLE 1,Install and Import Libraries
# Install required libraries
%pip install requests pandas --quiet

# Import libraries
import requests
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, current_timestamp
from datetime import datetime
import time

print("✓ Libraries imported successfully")

# COMMAND ----------

# DBTITLE 1,Define World Bank API Functions
def fetch_worldbank_data(indicator_code, start_year=1960, end_year=2024):
    """
    Fetch data from World Bank API for a specific indicator.
    
    Args:
        indicator_code: World Bank indicator code (e.g., 'NY.GDP.MKTP.CD')
        start_year: Start year for time series
        end_year: End year for time series
    
    Returns:
        DataFrame with country_code, country_name, year, value
    """
    base_url = "https://api.worldbank.org/v2"
    all_data = []
    page = 1
    per_page = 1000
    
    print(f"Fetching {indicator_code} data...")
    
    while True:
        # Construct API URL
        url = f"{base_url}/country/all/indicator/{indicator_code}"
        params = {
            'date': f"{start_year}:{end_year}",
            'format': 'json',
            'per_page': per_page,
            'page': page
        }
        
        # Make request
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            break
        
        data = response.json()
        
        # First element contains pagination info, second contains data
        if len(data) < 2 or not data[1]:
            break
        
        pagination_info = data[0]
        records = data[1]
        
        # Extract relevant fields
        for record in records:
            if record['value'] is not None:  # Skip null values
                all_data.append({
                    'country_code': record['countryiso3code'],
                    'country_name': record['country']['value'],
                    'year': int(record['date']),
                    'value': float(record['value']),
                    'indicator_code': indicator_code
                })
        
        print(f"  Page {page}/{pagination_info['pages']} - Retrieved {len(records)} records")
        
        # Check if there are more pages
        if page >= pagination_info['pages']:
            break
        
        page += 1
        time.sleep(1)  # Be nice to the API
    
    print(f"✓ Total records fetched: {len(all_data)}")
    return pd.DataFrame(all_data)


def filter_countries_only(df):
    """
    Filter out regional aggregates, keeping only country-level data.
    World Bank uses empty country codes for aggregates.
    """
    # Filter: keep only records with valid 3-letter country codes
    df_filtered = df[df['country_code'].str.len() == 3].copy()
    
    # Additional filter: exclude known aggregates
    aggregates_to_exclude = [
        'WLD',  # World
        'EAS',  # East Asia & Pacific
        'ECS',  # Europe & Central Asia
        'LCN',  # Latin America & Caribbean
        'MEA',  # Middle East & North Africa
        'NAC',  # North America
        'SAS',  # South Asia
        'SSF',  # Sub-Saharan Africa
        'HIC',  # High income
        'LIC',  # Low income
        'LMC',  # Lower middle income
        'MIC',  # Middle income
        'UMC',  # Upper middle income
        'ARB',  # Arab World
        'CSS',  # Caribbean small states
        'EUU',  # European Union
        'FCS',  # Fragile and conflict affected situations
        'HPC',  # Heavily indebted poor countries
        'IBD',  # IBRD only
        'IBT',  # IDA & IBRD total
        'IDA',  # IDA total
        'IDB',  # IDA blend
        'IDX',  # IDA only
        'LAC',  # Latin America & Caribbean (all income levels)
        'LDC',  # Least developed countries
        'LMY',  # Low & middle income
        'LTE',  # Late-demographic dividend
        'OED',  # OECD members
        'OSS',  # Other small states
        'PRE',  # Pre-demographic dividend
        'PSS',  # Pacific island small states
        'PST',  # Post-demographic dividend
        'SSA',  # Sub-Saharan Africa (all income levels)
        'SST',  # Small states
        'TEA',  # East Asia & Pacific (IDA & IBRD countries)
        'TEC',  # Europe & Central Asia (IDA & IBRD countries)
        'TLA',  # Latin America & the Caribbean (IDA & IBRD countries)
        'TMN',  # Middle East & North Africa (IDA & IBRD countries)
        'TSA',  # South Asia (IDA & IBRD)
        'TSS',  # Sub-Saharan Africa (IDA & IBRD countries)
    ]
    
    df_filtered = df_filtered[~df_filtered['country_code'].isin(aggregates_to_exclude)]
    
    print(f"✓ Filtered: {len(df)} → {len(df_filtered)} records (removed {len(df) - len(df_filtered)} aggregates)")
    return df_filtered

print("✓ API functions defined")

# COMMAND ----------

# DBTITLE 1,Improved API Function with Retry
def fetch_worldbank_data_robust(indicator_code, start_year=1960, end_year=2024):
    """
    Fetch data from World Bank API with robust error handling.
    Uses country-level endpoint to avoid regional aggregates.
    """
    base_url = "https://api.worldbank.org/v2"
    all_data = []
    page = 1
    per_page = 500
    max_retries = 3
    
    print(f"Fetching {indicator_code} data...")
    
    while True:
        url = f"{base_url}/country/all/indicator/{indicator_code}"
        params = {
            'date': f"{start_year}:{end_year}",
            'format': 'json',
            'per_page': per_page,
            'page': page
        }
        
        # Retry logic
        success = False
        for attempt in range(max_retries):
            try:
                response = requests.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    success = True
                    break
                elif response.status_code in [429, 503]:
                    wait_time = 2 ** attempt
                    print(f"  Rate limited (page {page}), waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"  Error {response.status_code} (page {page}, attempt {attempt+1})")
                    time.sleep(2)
            except Exception as e:
                print(f"  Exception (page {page}, attempt {attempt+1}): {str(e)[:50]}")
                time.sleep(2)
        
        if not success:
            print(f"❌ Failed after {max_retries} attempts on page {page}. Stopping.")
            break
        
        data = response.json()
        
        if len(data) < 2 or not data[1]:
            break
        
        pagination_info = data[0]
        records = data[1]
        
        for record in records:
            if record['value'] is not None:
                all_data.append({
                    'country_code': record['countryiso3code'],
                    'country_name': record['country']['value'],
                    'year': int(record['date']),
                    'value': float(record['value']),
                    'indicator_code': indicator_code
                })
        
        print(f"  ✓ Page {page}/{pagination_info['pages']} - {len(records)} records")
        
        if page >= pagination_info['pages']:
            break
        
        page += 1
        time.sleep(1)
    
    print(f"✓ Total records fetched: {len(all_data)}")
    return pd.DataFrame(all_data)


def filter_countries_only_improved(df):
    """
    Filter to keep ONLY individual countries, removing ALL regional/income aggregates.
    Uses multiple strategies:
    1. Valid 3-letter ISO codes
    2. Exclude known aggregate prefixes
    3. Exclude specific aggregate codes
    """
    original_count = len(df)
    
    # Strategy 1: Keep only 3-letter codes
    df_filtered = df[df['country_code'].str.len() == 3].copy()
    
    # Strategy 2: Exclude aggregate prefixes
    # World Bank uses specific patterns for aggregates
    aggregate_prefixes = ['X', 'Z', 'V']  # Common aggregate prefixes
    for prefix in aggregate_prefixes:
        df_filtered = df_filtered[~df_filtered['country_code'].str.startswith(prefix)]
    
    # Strategy 3: Explicit exclusion list (comprehensive)
    aggregates = [
        # Regional aggregates
        'AFE', 'AFW', 'ARB', 'CSS', 'EAP', 'EAS', 'ECA', 'ECS', 'EMU', 'EUU',
        'FCS', 'HPC', 'LAC', 'LCN', 'LDC', 'MEA', 'MNA', 'NAC', 'OED', 'OSS',
        'PSS', 'SAS', 'SSA', 'SSF', 'SST', 'TEA', 'TEC', 'TLA', 'TMN', 'TSA', 'TSS',
        # Income aggregates
        'HIC', 'INX', 'LIC', 'LMC', 'LMY', 'MIC', 'UMC',
        # Lending aggregates
        'IBD', 'IBT', 'IDA', 'IDB', 'IDX',
        # Demographic aggregates
        'EAR', 'LTE', 'PRE', 'PST',
        # World
        'WLD',
        # Other aggregates
        'CEB', 'CEA', 'CEU', 'CAA', 'CAF', 'CSA', 'CLA'
    ]
    
    df_filtered = df_filtered[~df_filtered['country_code'].isin(aggregates)]
    
    filtered_count = len(df_filtered)
    removed = original_count - filtered_count
    
    print(f"✓ Filtered: {original_count} → {filtered_count} records (removed {removed} aggregates)")
    
    # Show sample to verify
    unique_countries = df_filtered['country_code'].nunique()
    print(f"  Unique countries: {unique_countries}")
    
    return df_filtered

print("✓ Improved functions defined")

# COMMAND ----------

# DBTITLE 1,Download GDP Total Data
# Download GDP (current US$) - Indicator: NY.GDP.MKTP.CD
print("="*70)
print("DOWNLOADING: GDP Total (current US$)")
print("="*70)

gdp_total_df = fetch_worldbank_data_robust('NY.GDP.MKTP.CD', start_year=1960, end_year=2024)
gdp_total_df = filter_countries_only_improved(gdp_total_df)

# Rename value column
gdp_total_df = gdp_total_df.rename(columns={'value': 'gdp_usd'})

print(f"\n✓ GDP Total data ready: {len(gdp_total_df)} records")
print(f"  Countries: {gdp_total_df['country_code'].nunique()}")
print(f"  Year range: {gdp_total_df['year'].min()} - {gdp_total_df['year'].max()}")
print(f"\nSample:")
display(gdp_total_df.head(10))

# COMMAND ----------

# DBTITLE 1,Download GDP Per Capita Data
# Download GDP per capita (current US$) - Indicator: NY.GDP.PCAP.CD
print("="*70)
print("DOWNLOADING: GDP Per Capita (current US$)")
print("="*70)

gdp_per_capita_df = fetch_worldbank_data_robust('NY.GDP.PCAP.CD', start_year=1960, end_year=2024)
gdp_per_capita_df = filter_countries_only_improved(gdp_per_capita_df)

# Rename value column
gdp_per_capita_df = gdp_per_capita_df.rename(columns={'value': 'gdp_per_capita_usd'})

print(f"\n✓ GDP Per Capita data ready: {len(gdp_per_capita_df)} records")
print(f"  Countries: {gdp_per_capita_df['country_code'].nunique()}")
print(f"  Year range: {gdp_per_capita_df['year'].min()} - {gdp_per_capita_df['year'].max()}")
print(f"\nSample:")
display(gdp_per_capita_df.head(10))

# COMMAND ----------

# DBTITLE 1,Create Delta Tables in Unity Catalog
# Metadata
download_timestamp = datetime.now().isoformat()
data_source = "World Bank Open Data"
data_source_url = "https://data.worldbank.org"

print("="*70)
print("CREATING DELTA TABLES IN UNITY CATALOG")
print("="*70)

# Convert pandas to Spark DataFrames
print("\n1. Converting to Spark DataFrames...")
spark_gdp_total = spark.createDataFrame(gdp_total_df)
spark_gdp_per_capita = spark.createDataFrame(gdp_per_capita_df)

# Add metadata columns
spark_gdp_total = spark_gdp_total \
    .withColumn('data_source', lit(data_source)) \
    .withColumn('data_source_url', lit(data_source_url)) \
    .withColumn('download_timestamp', lit(download_timestamp)) \
    .withColumn('created_at', current_timestamp())

spark_gdp_per_capita = spark_gdp_per_capita \
    .withColumn('data_source', lit(data_source)) \
    .withColumn('data_source_url', lit(data_source_url)) \
    .withColumn('download_timestamp', lit(download_timestamp)) \
    .withColumn('created_at', current_timestamp())

# Reorder columns
spark_gdp_total = spark_gdp_total.select(
    'country_code', 'country_name', 'year', 'gdp_usd', 'indicator_code',
    'data_source', 'data_source_url', 'download_timestamp', 'created_at'
)

spark_gdp_per_capita = spark_gdp_per_capita.select(
    'country_code', 'country_name', 'year', 'gdp_per_capita_usd', 'indicator_code',
    'data_source', 'data_source_url', 'download_timestamp', 'created_at'
)

print("✓ Spark DataFrames ready")

# Create tables in Unity Catalog
print("\n2. Creating table: geopolitics_data_catalog.processed.world_gdp_total")
spark_gdp_total.write \
    .format('delta') \
    .mode('overwrite') \
    .option('overwriteSchema', 'true') \
    .saveAsTable('geopolitics_data_catalog.processed.world_gdp_total')
print("✓ Table created successfully")

print("\n3. Creating table: geopolitics_data_catalog.processed.world_gdp_per_capita")
spark_gdp_per_capita.write \
    .format('delta') \
    .mode('overwrite') \
    .option('overwriteSchema', 'true') \
    .saveAsTable('geopolitics_data_catalog.processed.world_gdp_per_capita')
print("✓ Table created successfully")

print("\n" + "="*70)
print("✓ ALL TABLES CREATED IN geopolitics_data_catalog.processed")
print("="*70)

# COMMAND ----------

# DBTITLE 1,Validation Queries
# MAGIC %sql
# MAGIC -- Validation: GDP Total Table
# MAGIC SELECT 
# MAGIC     'world_gdp_total' AS table_name,
# MAGIC     COUNT(*) AS total_records,
# MAGIC     COUNT(DISTINCT country_code) AS unique_countries,
# MAGIC     MIN(year) AS min_year,
# MAGIC     MAX(year) AS max_year,
# MAGIC     MIN(gdp_usd) AS min_gdp,
# MAGIC     MAX(gdp_usd) AS max_gdp,
# MAGIC     MAX(data_source) AS data_source,
# MAGIC     MAX(indicator_code) AS indicator_code
# MAGIC FROM geopolitics_data_catalog.processed.world_gdp_total
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC -- Validation: GDP Per Capita Table
# MAGIC SELECT 
# MAGIC     'world_gdp_per_capita' AS table_name,
# MAGIC     COUNT(*) AS total_records,
# MAGIC     COUNT(DISTINCT country_code) AS unique_countries,
# MAGIC     MIN(year) AS min_year,
# MAGIC     MAX(year) AS max_year,
# MAGIC     MIN(gdp_per_capita_usd) AS min_gdp,
# MAGIC     MAX(gdp_per_capita_usd) AS max_gdp,
# MAGIC     MAX(data_source) AS data_source,
# MAGIC     MAX(indicator_code) AS indicator_code
# MAGIC FROM geopolitics_data_catalog.processed.world_gdp_per_capita

# COMMAND ----------

# DBTITLE 1,Sample Data Preview
# MAGIC %sql
# MAGIC -- Top 10 countries by GDP (most recent year available)
# MAGIC WITH latest_year AS (
# MAGIC     SELECT MAX(year) AS max_year
# MAGIC     FROM geopolitics_data_catalog.processed.world_gdp_total
# MAGIC )
# MAGIC SELECT 
# MAGIC     country_name,
# MAGIC     country_code,
# MAGIC     year,
# MAGIC     ROUND(gdp_usd / 1e12, 2) AS gdp_trillion_usd,
# MAGIC     indicator_code
# MAGIC FROM geopolitics_data_catalog.processed.world_gdp_total
# MAGIC WHERE year = (SELECT max_year FROM latest_year)
# MAGIC ORDER BY gdp_usd DESC
# MAGIC LIMIT 10

# COMMAND ----------

# DBTITLE 1,Verify European Countries 1960-2024
# MAGIC %sql
# MAGIC -- Verify data availability for the 6 European countries from 1960
# MAGIC SELECT 
# MAGIC     country_code,
# MAGIC     country_name,
# MAGIC     MIN(year) as first_year,
# MAGIC     MAX(year) as last_year,
# MAGIC     COUNT(*) as total_records
# MAGIC FROM geopolitics_data_catalog.processed.world_gdp_total
# MAGIC WHERE country_code IN ('ITA', 'FRA', 'DEU', 'NLD', 'GBR', 'ESP')
# MAGIC GROUP BY country_code, country_name
# MAGIC ORDER BY country_code

# COMMAND ----------

# DBTITLE 1,Italy GDP Historical Trend
# MAGIC %sql
# MAGIC -- Italy GDP historical trend (last 20 years)
# MAGIC SELECT 
# MAGIC     t.year,
# MAGIC     ROUND(t.gdp_usd / 1e9, 2) AS gdp_billion_usd,
# MAGIC     ROUND(p.gdp_per_capita_usd, 2) AS gdp_per_capita_usd
# MAGIC FROM geopolitics_data_catalog.processed.world_gdp_total t
# MAGIC LEFT JOIN geopolitics_data_catalog.processed.world_gdp_per_capita p
# MAGIC     ON t.country_code = p.country_code AND t.year = p.year
# MAGIC WHERE t.country_code = 'ITA'
# MAGIC     AND t.year >= 2004
# MAGIC ORDER BY t.year DESC