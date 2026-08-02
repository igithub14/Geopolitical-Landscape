#!/usr/bin/env python3

import os
from pathlib import Path

import requests

OUTPUT_DIR = Path(".github/scripts/exports")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value.strip() == "":
        raise SystemExit(f"Missing required environment variable: {name}")
    return value.strip()


def fetch_dashboard_export(host: str, token: str, dashboard_id: str) -> bytes:
    url = f"{host.rstrip('/')}/api/2.0/preview/sql/dashboards/export"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "text/html",
    }
    params = {
        "dashboard_id": dashboard_id,
        "format": "HTML",
    }

    response = requests.get(url, headers=headers, params=params, timeout=60)
    response.raise_for_status()
    return response.content


def main() -> None:
    host = get_env("DATABRICKS_HOST")
    token = get_env("DATABRICKS_TOKEN")
    dashboard_ids = get_env("DATABRICKS_DASHBOARD_IDS")

    for raw_id in dashboard_ids.split(","):
        dashboard_id = raw_id.strip()
        if not dashboard_id:
            continue

        print(f"Exporting dashboard {dashboard_id}...")
        output = fetch_dashboard_export(host, token, dashboard_id)
        path = OUTPUT_DIR / f"dashboard-{dashboard_id}.html"
        path.write_bytes(output)
        print(f"Saved: {path}")

    print(f"Export complete. Files written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
