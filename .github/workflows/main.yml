name: Premium Ad Clicker Runner

on:
  workflow_dispatch:
  schedule:
    - cron: '0 */3 * * *'

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install System Dependencies
        run: |
          sudo apt-get update
          # Chrome aur dependencies install karne ka behtar tareeka
          sudo apt-get install -y xvfb x11-utils google-chrome-stable || true
          # Package name fix for Ubuntu 24.04 (libasound2 vs libasound2t64)
          sudo apt-get install -y libnss3 libatk-bridge2.0-0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2t64 || sudo apt-get install -y libasound2 || true

      - name: Install Python Requirements
        run: |
          pip install -r requirements.txt

      - name: Run Bot with Virtual Display
        env:
          GITHUB_ACTIONS: "true"
        run: |
          xvfb-run --server-args="-screen 0 1920x1080x24" python ad_clicker.py --query "https://abr.ge/zz4y46"
