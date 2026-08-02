# Script to export Databricks dashboard HTML pages
# Usage: set secrets DATABRICKS_DASHBOARD_URLS (comma-separated URLs) and DATABRICKS_TOKEN

import os
import argparse
import requests
from urllib.parse import urlparse

def slugify(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.replace('/', '_').strip('_')
    if not path:
        path = parsed.netloc
    return f"{parsed.netloc}-{path}.html"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='./docs', help='Output directory for exported HTML')
    args = parser.parse_args()

    out_dir = args.out
    os.makedirs(out_dir, exist_ok=True)

    dashboard_urls = os.environ.get('DATABRICKS_DASHBOARD_URLS')
    token = os.environ.get('DATABRICKS_TOKEN') or os.environ.get('DATABRICKS_TOKEN')

    if not dashboard_urls:
        print('No DATABRICKS_DASHBOARD_URLS env var set. Nothing to do.')
        return
    if not token:
        print('Warning: DATABRICKS_TOKEN not set. Attempting unauthenticated fetch.')

    urls = [u.strip() for u in dashboard_urls.split(',') if u.strip()]

    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'

    for url in urls:
        try:
            print(f'Fetching: {url}')
            resp = requests.get(url, headers=headers, timeout=60)
            resp.raise_for_status()
            filename = slugify(url)
            out_path = os.path.join(out_dir, filename)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(resp.text)
            print(f'Saved to {out_path}')
        except Exception as e:
            print(f'Failed to fetch {url}: {e}')

if __name__ == '__main__':
    main()
