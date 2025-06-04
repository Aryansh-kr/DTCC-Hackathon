from neo4j import GraphDatabase

# Connect to your Neo4j instance
uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"  # Replace with your actual password

driver = GraphDatabase.driver(uri, auth=(username, password))

# Define your triplets
triplets = [
    {"subject": "ESMA", "predicate": "issued", "object": "Guidelines on Enforcement of Financial Information"},
    {"subject": "Guidelines", "predicate": "apply to", "object": "competent authorities of EU Member States"},
    {"subject": "Guidelines", "predicate": "apply to", "object": "competent authorities of EEA countries"},
    {"subject": "Guidelines", "predicate": "enforce", "object": "financial information under Transparency Directive"},
    {"subject": "Transparency Directive", "predicate": "requires", "object": "issuers' financial information to comply with financial reporting framework"},
    {"subject": "Competent authorities", "predicate": "must ensure", "object": "effective enforcement of financial information"},
    {"subject": "Enforcer", "predicate": "examines", "object": "compliance of financial information"},
    {"subject": "Enforcer", "predicate": "takes", "object": "appropriate measures on detecting infringements"},
    {"subject": "Financial information", "predicate": "must comply with", "object": "IFRS or equivalent GAAP"},
    {"subject": "Guidelines", "predicate": "exclude", "object": "non-financial statements under Articles 19a and 29a of Accounting Directive"},
    {"subject": "EECS", "predicate": "coordinates", "object": "European enforcement practices"},
    {"subject": "EECS", "predicate": "discusses", "object": "emerging issues and enforcement decisions"},
    {"subject": "Enforcers", "predicate": "must have", "object": "sufficient human and financial resources"},
    {"subject": "Enforcers", "predicate": "must ensure", "object": "independence from government and market participants"},
    {"subject": "Enforcer", "predicate": "may issue", "object": "corrective note for material misstatement"},
    {"subject": "Selection model", "predicate": "combines", "object": "risk-based, sampling and rotation approaches"},
    {"subject": "Examinations", "predicate": "include", "object": "interactive and desktop procedures"},
    {"subject": "Interactive unlimited examinations", "predicate": "should cover", "object": "at least 33% of annual examinations or 10% of issuers"},
    {"subject": "Enforcer", "predicate": "uses", "object": "Guideline 7 actions for material misstatements"},
    {"subject": "Material misstatement", "predicate": "triggers", "object": "reissuance, corrective note, or correction in future statements"},
    {"subject": "ESMA", "predicate": "coordinates", "object": "common enforcement priorities"},
    {"subject": "Emerging issue", "predicate": "must be discussed in", "object": "EECS before decision is taken"},
    {"subject": "Enforcement decisions", "predicate": "must consider", "object": "previous similar decisions"},
    {"subject": "Enforcement decisions", "predicate": "must be submitted to", "object": "ESMA"},
    {"subject": "European enforcers", "predicate": "report", "object": "enforcement activities to ESMA"}
]

# Sanitize predicate to be a valid Cypher relationship type
def sanitize_predicate(predicate):
    return predicate.upper().replace(" ", "_").replace("-", "_").replace("'", "").replace("%", "PERCENT")

# Function to create nodes and relationships
def create_knowledge_graph(tx, subject, predicate, object_):
    rel_type = sanitize_predicate(predicate)
    query = f"""
        MERGE (a:Entity {{name: $subject}})
        MERGE (b:Entity {{name: $object}})
        MERGE (a)-[:{rel_type}]->(b)
    """
    tx.run(query, subject=subject, object=object_)

# Run the insertion
with driver.session() as session:
    for triplet in triplets:
        session.write_transaction(create_knowledge_graph, triplet["subject"], triplet["predicate"], triplet["object"])

driver.close()
