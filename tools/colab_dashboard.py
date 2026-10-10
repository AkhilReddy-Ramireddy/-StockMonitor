#!/usr/bin/env python3
"""
Colab Dashboard Display for StockMonitor
Run this in a Colab cell to display the live dashboard.
"""

import os
import json
from google.colab import output

def display_dashboard():
    """Display the dashboard HTML in Colab output cell."""

    # Read the HTML file
    html_path = 'dashboard.html'
    if not os.path.exists(html_path):
        # Try to find it
        for root, dirs, files in os.walk('.'):
            if 'dashboard.html' in files:
                html_path = os.path.join(root, 'dashboard.html')
                break

    if os.path.exists(html_path):
        with open(html_path, 'r') as f:
            html_content = f.read()

        # Inject Colab-specific modifications
        # The dashboard uses fetch() which won't work in Colab iframe
        # We'll inject the data directly
        portfolio_path = os.environ.get('STOCKMONITOR_DATA_DIR', 'session') + '/portfolio.json'

        portfolio_data = {"cash": 1000, "positions": {}, "data_mode": "LIVE"}
        trades_data = []

        if os.path.exists(portfolio_path):
            with open(portfolio_path, 'r') as f:
                portfolio_data = json.load(f)

        trades_path = os.environ.get('STOCKMONITOR_DATA_DIR', 'session') + '/trades.csv'
        if os.path.exists(trades_path):
            import csv
            with open(trades_path, 'r') as f:
                reader = csv.DictReader(f)
                trades_data = list(reader)

        # Inject data into HTML
        injection_script = f"""
        <script>
        // Override fetch to use injected data
        window.__PORTFOLIO_DATA__ = {json.dumps(portfolio_data)};
        window.__TRADES_DATA__ = {json.dumps(trades_data)};

        // Auto-refresh disabled in Colab
        document.addEventListener('DOMContentLoaded', () => {{
            // The existing JS will render this
        }});
        </script>
        """

        # Insert before closing body
        html_content = html_content.replace('</body>', injection_script + '\n</body>')

        output.display_html(html_content, raw=True)
        print("✅ Dashboard displayed above. Re-run this cell to refresh.")
    else:
        print("❌ dashboard.html not found. Upload it to your project directory.")

def refresh_dashboard():
    """Quick refresh function."""
    display_dashboard()

# Quick usage in Colab:
# from tools.colab_dashboard import display_dashboard, refresh_dashboard
# display_dashboard()
# # After trades:
# refresh_dashboard()