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
