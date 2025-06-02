import networkx as nx
import matplotlib.pyplot as plt

# Sample knowledge triplets
triplets = [
    {"subject": "ESMA", "predicate": "issued", "object": "Guidelines on enforcement of financial information"},
    {"subject": "Guidelines", "predicate": "apply to", "object": "competent authorities of EU and EEA Member States"},
    {"subject": "Guidelines", "predicate": "relate to", "object": "enforcement of financial information under the Transparency Directive"},
    {"subject": "Enforcement of financial information", "predicate": "ensures", "object": "compliance with financial reporting framework"},
    {"subject": "Transparency Directive", "predicate": "requires", "object": "publication of harmonised financial information"},
    {"subject": "EECS", "predicate": "coordinates", "object": "European enforcement discussions"},
    {"subject": "Enforcer", "predicate": "examines", "object": "issuer's financial information"},
    {"subject": "Enforcer", "predicate": "takes", "object": "enforcement actions when infringements are found"},
    {"subject": "CESR", "predicate": "developed", "object": "Standards No. 1 and 2 on enforcement"},
    {"subject": "ESMA", "predicate": "coordinates", "object": "enforcement activities across Member States"}
]

# Create directed graph
G = nx.DiGraph()

# Add nodes and edges
for triplet in triplets:
    G.add_node(triplet["subject"])
    G.add_node(triplet["object"])
    G.add_edge(triplet["subject"], triplet["object"], label=triplet["predicate"])

# Set layout
pos = nx.spring_layout(G, k=1.2, seed=42)

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=2000, alpha=0.8)

# Draw edges
nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowstyle='-|>', arrowsize=15)

# Draw node labels
nx.draw_networkx_labels(G, pos, font_size=9, font_family='sans-serif')

# Draw edge labels (predicates)
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='darkgreen', font_size=8)

# Show plot
plt.title("Knowledge Graph of ESMA Guidelines", fontsize=14)
plt.axis('off')
plt.tight_layout()
plt.show()
