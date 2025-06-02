from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

class GraphLoader:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        self.driver.close()

    def clear_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def insert_entities_and_relationships(self, triples):
        with self.driver.session() as session:
            for subj, rel, obj in triples:
                session.run(
                    """
                    MERGE (a:Entity {name: $subj})
                    MERGE (b:Entity {name: $obj})
                    MERGE (a)-[:RELATION {type: $rel}]->(b)
                    """,
                    subj=subj, rel=rel, obj=obj
                )
