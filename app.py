from flask import Flask, render_template, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j credentials
uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(username, password))

def get_graph_data():
    with driver.session() as session:
        result = session.run("MATCH (a)-[r]->(b) RETURN a, r, b LIMIT 100")
        nodes = {}
        edges = []

        for record in result:
            a = record["a"]
            b = record["b"]
            r = record["r"]

            # Add node a
            if a.id not in nodes:
                nodes[a.id] = {
                    "id": a.id,
                    "label": a.get("name") or a.get("title") or "Entity",
                    "group": list(a.labels)[0] if a.labels else "Node"
                }

            # Add node b
            if b.id not in nodes:
                nodes[b.id] = {
                    "id": b.id,
                    "label": b.get("name") or b.get("title") or "Entity",
                    "group": list(b.labels)[0] if b.labels else "Node"
                }

            # Add edge
            edges.append({
                "from": a.id,
                "to": b.id,
                "label": r.type
            })

        return {"nodes": list(nodes.values()), "edges": edges}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/graph-data")
def graph_data():
    data = get_graph_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
