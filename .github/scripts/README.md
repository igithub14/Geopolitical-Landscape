# GitHub Scripts

This folder contains scripts used by GitHub Actions for the Geopolitical-Landscape repository.

## Export dashboards

- `.github/workflows/databricks-export.yml`: workflow that exports Databricks dashboards on demand.
- `.github/scripts/export_dashboards.py`: Python helper script that downloads dashboard exports and writes HTML files.

## Required secrets

The workflow expects the following repository secrets:

- `DATABRICKS_HOST`: the Databricks workspace URL, for example `https://adb-123456789012345.7.azuredatabricks.net`.
- `DATABRICKS_TOKEN`: a Databricks personal access token with SQL dashboard export permissions.
- `DATABRICKS_DASHBOARD_IDS`: comma-separated dashboard IDs to export.

## Output

Exported dashboards are written to `.github/scripts/exports/` and uploaded as workflow artifacts.
