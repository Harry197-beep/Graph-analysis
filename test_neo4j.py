from neo4j import GraphDatabase
from database import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

try:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    driver.verify_connectivity()
    print("✓ Connection successful!")
    driver.close()
except Exception as e:
    print(f"✗ Connection failed: {e}")