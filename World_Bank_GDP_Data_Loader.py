name: Deploy Hugo site with Python dashboards

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

defaults:
  run:
    shell: bash

jobs:
  build:
    runs-on: ubuntu-latest

    env:
      HUGO_VERSION: 0.128.0

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          submodules: recursive

      # -------------------------
      # INSTALL PYTHON + JUPYTER
      # -------------------------
      - name: Install Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install Jupyter + nbconvert
        run: |
          pip install jupyter nbconvert

      # -----------------------------------------
      # EXECUTE PY SCRIPTS (if they generate output)
      # -----------------------------------------
      - name: Run Python scripts
        run: |
          python Political_Network_Data_Loader.py || true

      # -----------------------------------------
      # CONVERT SPECIFIC NOTEBOOKS TO HTML
      # -----------------------------------------
      - name: Convert notebooks to HTML
        run: |
          mkdir -p static/dashboards

          jupyter nbconvert --to html GovernmentDurationMetrics.ipynb \
            --output GovernmentDurationMetrics.html
          mv GovernmentDurationMetrics.html static/dashboards/

          jupyter nbconvert --to html Eurostat_GDP_Volume_Loader.ipynb \
            --output Eurostat_GDP_Volume_Loader.html
          mv Eurostat_GDP_Vol
