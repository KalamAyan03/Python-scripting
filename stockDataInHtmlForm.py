import yfinance as yf
import pandas as pd
import webbrowser
import os

def generate_full_html_report(ticker_symbol):
    print(f"--- 🚀 Fetching Intelligence for {ticker_symbol} ---")
    stock = yf.Ticker(ticker_symbol)
    
    # ==============================
    # 1. FETCH ALL DATA POINTS
    # ==============================
    info = stock.info
    
    # DataFrames (Tables)
    balance_sheet = stock.balance_sheet
    financials = stock.financials
    cashflow = stock.cashflow
    major_holders = stock.major_holders
    
    # Events & Calendar (Point 6 & 9)
    calendar = stock.calendar
    
    # History (Point 7) - Last 10 days of trading
    history = stock.history(period="1mo").tail(10)
    # Cleaning up history (rounding numbers for readability)
    history = history[['Open', 'High', 'Low', 'Close', 'Volume']].round(2)
    
    # News (Point 8)
    news_list = stock.get_news()
    
    # ==============================
    # 2. BUILD HTML REPORT
    # ==============================
    html_content = f"""
    <html>
    <head>
        <title>{ticker_symbol} Deep Dive Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f0f2f5; color: #333; }}
            h1 {{ color: #2c3e50; border-bottom: 4px solid #3498db; padding-bottom: 10px; }}
            h2 {{ color: #16a085; margin-top: 40px; border-left: 6px solid #16a085; padding-left: 15px; background: #e8f6f3; padding-top: 5px; padding-bottom: 5px; }}
            .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            
            /* Table Styling */
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 0.9em; }}
            th {{ background-color: #34495e; color: white; padding: 12px; text-align: left; }}
            td {{ border: 1px solid #ddd; padding: 10px; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            tr:hover {{ background-color: #f1f1f1; }}

            /* News Styling */
            .news-item {{ margin-bottom: 15px; padding: 15px; background: #fff; border-left: 5px solid #e74c3c; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            a {{ text-decoration: none; color: #2980b9; font-weight: bold; }}
            a:hover {{ text-decoration: underline; color: #c0392b; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🕵️ Cyber Intelligence Report: {ticker_symbol}</h1>
            
            <h2>1. Company Profile (Info)</h2>
            <p><strong>Sector:</strong> {info.get('sector', 'N/A')}</p>
            <p><strong>Industry:</strong> {info.get('industry', 'N/A')}</p>
            <p><strong>Market Cap:</strong> ₹{info.get('marketCap', 'N/A'):,}</p>
            <p><strong>P/E Ratio:</strong> {info.get('trailingPE', 'N/A')}</p>
            <p><strong>Business Summary:</strong> {info.get('longBusinessSummary', 'N/A')}</p>

            <h2>2. Recent Market Data (History - Last 10 Days)</h2>
            {history.to_html() if not history.empty else "<p>No History Data</p>"}

            <h2>3. Balance Sheet (Assets vs Liabilities)</h2>
            {balance_sheet.head(5).to_html() if not balance_sheet.empty else "<p>No Balance Sheet Data</p>"}

            <h2>4. Financials (Profit & Loss)</h2>
            {financials.head(5).to_html() if not financials.empty else "<p>No Financial Data</p>"}

            <h2>5. Cashflow (Inflow/Outflow)</h2>
            {cashflow.head(5).to_html() if not cashflow.empty else "<p>No Cashflow Data</p>"}

            <h2>6. Major Holders (Ownership)</h2>
            {major_holders.to_html() if not major_holders.empty else "<p>No Holders Data</p>"}

            <h2>7. Upcoming Events (Calendar)</h2>
            <p><em>(Earnings dates and report releases)</em></p>
    """
    
    # Handling Calendar (It can be a Dict or DataFrame)
    if calendar:
        # Converting dictionary to a readable HTML table if needed
        if isinstance(calendar, dict):
             # Create a simple table for the dictionary
            html_content += "<table border='1'><tr><th>Event</th><th>Date/Value</th></tr>"
            for key, value in calendar.items():
                html_content += f"<tr><td>{key}</td><td>{value}</td></tr>"
            html_content += "</table>"
        else:
            # If it's already a list or object, just print it
            html_content += f"<pre>{calendar}</pre>"
    else:
        html_content += "<p>No upcoming calendar events found.</p>"

    html_content += """
            <h2>8. Latest Intelligence (News)</h2>
    """
    
    # News Loop
    if news_list:
        for news in news_list[:5]:
            title = news.get('title', 'No Title')
            link = news.get('link', '#')
            publisher = news.get('publisher', 'Unknown Source')
            html_content += f"""
            <div class="news-item">
                <a href="{link}" target="_blank">{title}</a><br>
                <small>Source: {publisher}</small>
            </div>
            """
    else:
        html_content += "<p>No news found.</p>"

    html_content += """
        </div>
    </body>
    </html>
    """

    # ==============================
    # 3. SAVE AND OPEN
    # ==============================
    filename = f"{ticker_symbol}_Full_Report.html"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    
    print(f"✅ Report Generated: {filename}")
    
    # Auto-open in browser
    full_path = os.path.abspath(filename)
    webbrowser.open('file://' + full_path)

# --- RUN FOR YOUR STOCKS ---
generate_full_html_report("NETWEB.NS")
generate_full_html_report("KAYNES.NS")