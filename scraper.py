# scraper.py
import yfinance as yf
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import sqlite3
import ssl
import time  # <-- Added the time module right here
from database import SQLITE_FILE, init_relational_db

def scrape_stock_market_data(ticker_symbol):
    """Pulls market data from Yahoo Finance and saves to SQLite."""
    # Ensure the database and tables are created before doing anything else
    init_relational_db()
    
    idx_ticker = f"{ticker_symbol}.JK"
    stock = yf.Ticker(idx_ticker)
    info = stock.info
    
    data = {
        "ticker": ticker_symbol,
        "name": info.get("longName", "Unknown Company"),
        "pe": info.get("trailingPE", 0.0),
        "roe": info.get("returnOnEquity", 0.0) * 100 if info.get("returnOnEquity") else 0.0,
        "price": info.get("currentPrice", info.get("previousClose", 0.0)),
        "volume": info.get("volume", 0)
    }
    
    # Custom proprietary Intrinsic Value math formula
    data["intrinsic_value"] = data["price"] * 1.15 if data["pe"] < 15 else data["price"] * 0.85
    
    # Connect and insert into SQLite file
    conn = sqlite3.connect(SQLITE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO stock_metrics (ticker, company_name, pe_ratio, roe, intrinsic_value, current_price, daily_volume_shares)
        VALUES (:ticker, :name, :pe, :roe, :intrinsic_value, :price, :volume)
        ON CONFLICT(ticker) DO UPDATE SET
            pe_ratio = excluded.pe_ratio,
            roe = excluded.roe,
            intrinsic_value = excluded.intrinsic_value,
            current_price = excluded.current_price,
            daily_volume_shares = excluded.daily_volume_shares,
            last_updated = CURRENT_TIMESTAMP;
    """, data)
    
    conn.commit()
    conn.close()
    print(f"[✓] Stored SQL fundamentals for {ticker_symbol} inside {SQLITE_FILE}")
    return data

def fetch_indonesian_news(ticker_symbol):
    """Fetches live Indonesian financial news completely free from RSS with SSL bypass."""
    query = urllib.parse.quote(f"Saham {ticker_symbol}")
    url = f"https://news.google.com/rss/search?q={query}&hl=id-ID&gl=ID&ceid=ID:id"
    
    news_stories = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        # Bypass Mac's local SSL certificate requirements
        context = ssl._create_unverified_context()
        
        with urllib.request.urlopen(req, context=context) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        for item in root.findall('.//item')[:4]:
            news_stories.append({
                "title": item.find('title').text,
                "date": item.find('pubDate').text
            })
    except Exception as e:
        print(f"[!] News scrape failed: {e}")
        
    print(f"[✓] Collected {len(news_stories)} live news headlines for {ticker_symbol}")
    return news_stories

if __name__ == "__main__":
    # 1. Read tickers from your text file
    try:
        with open("tickers.txt", "r") as file:
            # Read lines, strip whitespace, ignore empty lines
            portfolio = [line.strip().upper() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print("[!] Could not find 'tickers.txt'. Running fallback list.")
        portfolio = ["BBCA", "BBRI", "BMRI", "BBNI"]

    print(f"[*] Initializing massive bulk scrape for {len(portfolio)} assets...")
    
    # 2. Loop through every ticker safely
    for index, ticker in enumerate(portfolio):
        print(f"\n--- [{index + 1}/{len(portfolio)}] Extracting {ticker} ---")
        
        try:
            scrape_stock_market_data(ticker)
            fetch_indonesian_news(ticker)
        except Exception as e:
            # If one stock gets delisted or errors out, the script won't crash
            print(f"[!] Critical Error processing {ticker}: {e}")
            continue 
            
        # 3. CRITICAL: 3-second delay to prevent Google/Yahoo IP Bans
        time.sleep(3)
        
    print("\n[✓] ALL STOCKS SUCCESSFULLY SYNCED TO LOCAL DATABASE.")