# populate_graph.py
from neo4j import GraphDatabase
from database import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
def populate_idx_graph():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    print("[*] Connecting to Neo4j...")
    
    with driver.session() as session:
        # 1. Create the Conglomerate (The Parent)
        session.run("""
            MERGE (conglomerate:Conglomerate {name: 'Salim Group'})
        """)
        
        # 2. Create the Companies (Nodes)
        companies = [
            {"ticker": "BBCA", "name": "PT Bank Central Asia"},
            {"ticker": "INDF", "name": "PT Indofood Sukses Makmur"},
            {"ticker": "ASII", "name": "PT Astra International"}
        ]
        
        for comp in companies:
            session.run("""
                MERGE (c:Company {ticker: $ticker, name: $name})
            """, ticker=comp["ticker"], name=comp["name"])
            
            # Link Conglomerate to Company
            session.run("""
                MATCH (conglomerate:Conglomerate {name: 'Salim Group'})
                MATCH (c:Company {ticker: $ticker})
                MERGE (conglomerate)-[:OWNS_SHARES {percentage: 50}]->(c)
            """, ticker=comp["ticker"])

        # 3. Create the Directors (The Interlocking Network)
        # This is the "Gorengan" / Catalyst detector. 
        # We create a director who sits on MULTIPLE boards.
        directors = [
            {"name": "Johan H. Pratama", "boards": ["BBCA", "INDF"]}, # Interlocking!
            {"name": "Pembina Utama", "boards": ["ASII"]},
            {"name": "Anindya Bakrie", "boards": ["ASII", "BBCA"]} # Another Interlock!
        ]
        
        for director in directors:
            session.run("""
                MERGE (p:Person {name: $name})
            """, name=director["name"])
            
            for ticker in director["boards"]:
                session.run("""
                    MATCH (p:Person {name: $name})
                    MATCH (c:Company {ticker: $ticker})
                    MERGE (p)-[:SITS_ON_BOARD_OF]->(c)
                """, name=director["name"], ticker=ticker)

    driver.close()
    print("[✓] Successfully mapped corporate networks and interlocking directorates into Neo4j!")

if __name__ == "__main__":
    populate_idx_graph()