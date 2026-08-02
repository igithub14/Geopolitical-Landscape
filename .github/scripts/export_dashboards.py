#!/usr/bin/env python3
import os
from pathlib import Path
import requests
OUTPUT_DIR = Path(".github/scripts/exports")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or str(value).strip() == "":
        raise SystemExit(f"Missing required environment variable: {name}")
    return str(value).strip()
def fetch_dashboard_export(host: str, token: str, dashboard_id: str) -> bytes:
    url = f"{host.rstrip('/')}/api/2.0/preview/sql/dashboards/export"
    headers = {"Authorization": f"Bearer {token}", "Accept": "text/html"}
    params = {"dashboard_id": dashboard_id, "format": "HTML"}
    response = requests.get(url, headers=headers, params=params, timeout=60)
    response.raise_for_status()
    return response.content
def generate_index(output_dir: Path) -> None:
    files = sorted(output_dir.glob("dashboard-*.html"))
    index_path = output_dir / "index.html"
    with index_path.open("w", encoding="utf-8") as f:
        f.write("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n")
        f.write("<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n")
        f.write("<title>Exported Dashboards</title>\n</head>\n<body>\n")
        f.write("<h1>Exported Dashboards</h1>\n<ul>\n")
        for p in files:
            name = p.name
            f.write(f'  <li><a href=\"{name}\">{name}</a></li>\\n')
        f.write("</ul>\n</body>\n</html>\n")
    print(f\"Index generated: {index_path}\")
def main() -> None:
    host = get_env("DATABRICKS_HOST")
    token = get_env("DATABRICKS_TOKEN")
    dashboard_ids = get_env("DATABRICKS_DASHBOARD_IDS")
    for raw_id in str(dashboard_ids).split(","):
        dashboard_id = raw_id.strip()
        if not dashboard_id:
            continue
        print(f"Exporting dashboard {dashboard_id}...")
        output = fetch_dashboard_export(host, token, dashboard_id)
        path = OUTPUT_DIR / f"dashboard-{dashboard_id}.html"
        path.write_bytes(output)
        print(f"Saved: {path}")
    generate_index(OUTPUT_DIR)
    print(f"Export complete. Files written to: {OUTPUT_DIR}")
if __name__ == "__main__":
    main()
