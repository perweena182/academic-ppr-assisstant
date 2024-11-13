# backend/agents/db_agent.py

from neo4j import GraphDatabase
import os
import logging

class DBAgent:
    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Fetch environment variables or use default values
        uri = os.getenv("NEO4J_URI", "neo4j+s://dd959523.databases.neo4j.io")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "oPQCc42pb3wBJ1VD6_p50hEUSuJT_I6o7bKL3un5CJQ")
        
        # Initialize the Neo4j driver
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.logger.info("Successfully connected to Neo4j.")
        except Exception as e:
            self.logger.error(f"Failed to connect to Neo4j: {e}")
            raise e  # Re-raise exception after logging

    def store_papers(self, topic, papers):
        """
        Stores a list of papers under a specific topic in Neo4j.
        
        Parameters:
            topic (str): The research topic.
            papers (list): A list of dictionaries containing paper details.
        """
        with self.driver.session() as session:
            for paper in papers:
                try:
                    session.write_transaction(self._create_paper, topic, paper)
                    self.logger.info(f"Stored paper: {paper['title']}")
                except Exception as e:
                    self.logger.error(f"Failed to store paper '{paper['title']}': {e}")

    @staticmethod
    def _create_paper(tx, topic, paper):
        """
        Creates or merges Topic and Paper nodes and establishes a relationship.
        
        Parameters:
            tx: The transaction object.
            topic (str): The research topic.
            paper (dict): A dictionary containing paper details.
        """
        query = (
            "MERGE (t:Topic {name: $topic}) "
            "MERGE (p:Paper {title: $title, url: $url, published: $published}) "
            "MERGE (t)-[:HAS_PAPER]->(p)"
        )
        tx.run(query, topic=topic, title=paper['title'], url=paper['url'], published=paper['published'])

    
    def query_papers(self, topic, start_year=None, end_year=None):
        """
        Retrieves papers based on the topic and optional publication year range.
        
        Parameters:
            topic (str): The research topic.
            start_year (int, optional): The start year for publication date filtering.
            end_year (int, optional): The end year for publication date filtering.
        
        Returns:
            list: A list of papers matching the criteria.
        """
        with self.driver.session() as session:
            return session.read_transaction(self._get_papers, topic, start_year, end_year)

    @staticmethod
    def _get_papers(tx, topic, start_year, end_year):
        """
        Helper method to retrieve papers from Neo4j.
        
        Parameters:
            tx: The transaction object.
            topic (str): The research topic.
            start_year (int, optional): The start year for filtering.
            end_year (int, optional): The end year for filtering.
        
        Returns:
            list: A list of papers.
        """
        query = (
            "MATCH (t:Topic)-[:HAS_PAPER]->(p:Paper) "
            "WHERE t.name = $topic "
        )
        params = {"topic": topic}
        if start_year and end_year:
            query += "AND p.published >= $start_year AND p.published <= $end_year "
            params.update({
                "start_year": f"{start_year}-01-01",
                "end_year": f"{end_year}-12-31"
            })
        query += "RETURN p.title AS title, p.url AS url, p.published AS published ORDER BY p.published DESC"
        result = tx.run(query, **params)
        return [record for record in result]

# Initialize the DBAgent outside the class definition
db_agent = DBAgent()

