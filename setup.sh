#!/bin/bash

# Create directory structure
mkdir -p graphrag/{data,neo4j_utils,langchain_utils}

# Create .env file
cat > graphrag/.env <<EOL
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
OPENAI_API_KEY=your_openai_api_key
EOL

# Create requirements.txt
cat > graphrag/requirements.txt <<EOL
langchain
neo4j
openai
python-dotenv
tqdm
EOL

# Create sample document
cat > graphrag/data/sample_docs.txt <<EOL
Elon Musk founded SpaceX. SpaceX launched Falcon 9. Tesla is led by Elon Musk. Neuralink is another company founded by Elon Musk.
EOL

# Create __init__.py files
touch graphrag/neo4j_utils/__init__.py
touch graphrag/langchain_utils/__init__.py

# Create graph_loader.py
cat > graphrag/neo4j_utils/graph_loader.py <<'EOL'
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
EOL

# Create extract_graph.py
cat > graphrag/langchain_utils/extract_graph.py <<'EOL'
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))

EXTRACTION_PROMPT = """
Extract (subject, relation, object) triples from the following text.

Text:
{text}

Return the results as a list of triples like:
(subject1, relation1, object1)
(subject2, relation2, object2)
"""

prompt = PromptTemplate(
    input_variables=["text"],
    template=EXTRACTION_PROMPT
)

def extract_triples(text):
    formatted_prompt = prompt.format(text=text)
    response = llm.predict(formatted_prompt)
    
    # crude parsing — in practice use a parser or JSON output format
    triples = []
    for line in response.strip().split("\n"):
        if line.startswith("(") and line.endswith(")"):
            parts = line.strip("()").split(",")
            if len(parts) == 3:
                triples.append(tuple(part.strip().strip('"') for part in parts))
    return triples
EOL

# Create main.py
cat > graphrag/main.py <<'EOL'
from langchain_utils.extract_graph import extract_triples
from neo4j_utils.graph_loader import GraphLoader

def read_text(file_path):
    with open(file_path, "r") as f:
        return f.read()

def main():
    text = read_text("data/sample_docs.txt")
    triples = extract_triples(text)
    
    print("Extracted Triples:")
    for t in triples:
        print(t)
    
    graph_loader = GraphLoader()
    graph_loader.clear_database()
    graph_loader.insert_entities_and_relationships(triples)
    graph_loader.close()

if __name__ == "__main__":
    main()
EOL

echo "✅ GraphRAG project scaffold created with full code in 'graphrag/'"
