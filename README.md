# Graph-analysis
# IDX Institutional Intelligence & Asset Analyzer 📊🕸️

A quantitative and graph-based investment analysis platform for the Indonesia Stock Exchange (IDX). This system combines traditional fundamental analysis with **Neo4j graph network analysis** and **AI-driven reasoning** to uncover hidden corporate risks, interlocking directorates, and conglomerate contagion.

Designed to detect *gorengan* (wash-trading) traps and centralized corporate control, providing institutional-grade insights for retail and professional investors.

---

##  What It Does

1. **Fundamental Financial Analysis**: Pulls real-time financial metrics (P/E Ratio, ROE, Intrinsic Value, Volume) from local SQL databases to assess baseline stock health.
2. **Corporate Relationship Mapping**: Visualizes complex ownership structures and board memberships using a Neo4j graph database. It highlights who truly controls a company.
3. **Interlocking Directorate Detection**: Identifies individuals (Directors/Commissioners) who sit on multiple boards, revealing potential conflicts of interest or centralized control.
4. **AI Investment Advisory**: Uses Llama 3.1 (via Groq API) to synthesize fundamental data and graph network insights into a clear "CLEAR TO BUY" or "WARNING" recommendation with detailed reasoning.
5. **Interactive Dashboard**: A sleek, dark-themed frontend featuring interactive force-directed network graphs and dynamic financial trend charts.

---

## 🛠️ Tech Stack

### Backend & Data Processing
- **Python 3.13**: Core backend logic and data processing.
- **Flask**: Lightweight web framework serving the REST API (`/api/analyze/<ticker>`).
- **SQLite**: Stores historical fundamental financial data and daily market metrics (`idx_hedge_fund.db`).
- **idx-bei Scraper**: Custom Python scraping toolkit (`curl_cffi`, `BeautifulSoup4`) to extract real-time corporate profiles, directors, and ownership data directly from the official IDX website.

### Graph Database & AI
- **Neo4j AuraDB**: Cloud-hosted graph database used to map and query complex corporate relationships (`Company`, `Insider`, `Subsidiary` nodes and `OWNS`, `DIRECTOR_OF`, `COMMISSIONER_OF` edges).
- **Groq API (Llama 3.1)**: High-speed LLM inference engine used to generate the AI investment advisory and risk assessments.

### Frontend & Visualization
- **HTML5 / CSS3**: Custom dark-mode UI with glassmorphism, mesh gradients, and responsive grid layouts.
- **Typography**: Playfair Display (Editorial headings) & JetBrains Mono (Data/Technical text).
- **Vis.js**: Powers the interactive, hierarchical corporate network graphs.
- **Chart.js**: Renders dynamic financial trend charts (Earnings, Cash Flow).

---

## 🏗️ Architecture & Data Flow

1. **Data Ingestion**: The `idx-bei` scraper pulls raw corporate data from IDX and ingests it into **Neo4j** using `neo4j_ingest.py`.
2. **Financial Storage**: Historical stock prices and fundamental ratios are stored in **SQLite**.
3. **API Request**: The frontend sends a ticker symbol (e.g., `BBCA`) to the Flask backend (`analyzer.py`).
4. **Data Aggregation**: The backend queries SQLite for financials and Neo4j for the corporate network graph.
5. **AI Synthesis**: The aggregated data is passed to the Llama 3.1 prompt, which evaluates the stock and generates a recommendation.
6. **Visualization**: The frontend renders the metrics, charts, and the interactive Neo4j network graph.

---

## ️ Setup & Installation

### Prerequisites
- Python 3.13+
- Neo4j AuraDB Account (or local Neo4j instance)
- Groq API Key

### 1. Install Dependencies
```bash
pip3 install flask neo4j python-dotenv groq pandas sqlalchemy curl_cffi beautifulsoup4
Ensure your database.py and .env files contain your correct Neo4j AuraDB credentials:
python


123
NEO4J_URI = "neo4j+s://your-instance.databases.neo4j.io"NEO4J_USER = "neo4j"NEO4J_PASSWORD = "your-password"
3. Populate the Graph Database

Run the ingestion script to scrape IDX and populate Neo4j with real corporate data:
bash


12
cd idx-bei/pythonpython3 neo4j_ingest.py
4. Run the Application

Start the Flask API server:
bash

12
cd /path/to/Graph Analysispython3 analyzer.py
Open your browser and navigate to http://127.0.0.1:5001/.
🎯 Project Goals (Thesis Context)

This tool was built to test the hypothesis that traditional fundamental analysis is insufficient for the Indonesian market due to high conglomerate ownership and interlocking directorates. By layering graph network analysis over standard metrics, this system aims to:
Expose hidden "gorengan" (pump-and-dump) networks.
Identify systemic risks caused by conglomerate contagion.
Provide a transparent, data-driven alternative to traditional stock tips.
License


***

### How to use this:
1. Create a new file in your `Graph Analysis` folder named `README.md`.
2. Paste the code above into it.
3. If you are pushing this to GitHub, it will automatically render beautifully as your project's main page! 

MIT License. Built for educational and research purposes.  Disclaimer: This tool is for informational purposes only and does not constitute financial advice.
