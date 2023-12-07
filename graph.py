import rdflib
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt

g = Graph()
g.parse("ontology.ttl", format="turtle")  # Load ontology
result = g.parse("data1.ttl", format="turtle")  # Load existing data

user_uri = URIRef(f"http://example.org/User1")

G = rdflib_to_networkx_multidigraph(result)

# Plot Networkx instance of RDF Graph
pos = nx.spring_layout(G, scale=2)
edge_labels = nx.get_edge_attributes(G, 'r')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.draw(G, with_labels=True)

#if not in interactive mode for 
plt.show()