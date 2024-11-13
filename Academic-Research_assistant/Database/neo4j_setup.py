from neo4j import GraphDatabase
import os

def setup_neo4j():
    uri = os.getenv("NEO4J_URI", "neo4j+s://dd959523.databases.neo4j.io")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "oPQCc42pb3wBJ1VD6_p50hEUSuJT_I6o7bKL3un5CJQ")
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        # Create constraints using the new syntax
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Paper) REQUIRE p.url IS UNIQUE")
    driver.close()

if __name__ == "__main__":
    setup_neo4j()
    print("Neo4j setup completed.")
