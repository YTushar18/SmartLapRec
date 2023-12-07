"""
Visualizing RDF Graph with Networkx and Matplotlib

This script loads an RDF graph from ontology and data files, converts it to a Networkx graph,
and visualizes the graph using Matplotlib.

"""

import rdflib
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt

# Create an RDF graph and load ontology
g = Graph()
g.parse("ontology.ttl", format="turtle")

# Load existing data into the RDF graph
result = g.parse("data_graph.ttl", format="turtle")

# Define a user URI for demonstration
user_uri = URIRef(f"http://example.org/User1")

# Convert RDF graph to Networkx multidigraph
G = rdflib_to_networkx_multidigraph(result)

# Plot Networkx instance of RDF Graph
pos = nx.spring_layout(G, scale=2)
edge_labels = nx.get_edge_attributes(G, 'r')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.draw(G, with_labels=True)

# Display the plot
plt.show()