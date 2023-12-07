"""
CSV to RDF Conversion

This script reads laptop data from a CSV file, converts it into RDF triples,
and serializes the RDF graph to Turtle format.

"""

import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD

# Create a namespace for the project
ex = Namespace("http://example.org/")

# Read the CSV data
csv_file = "laptops.csv"
df = pd.read_csv(csv_file)

# Create an RDF graph
g = Graph()

# Define the RDF type for laptops
laptop_type = ex.Laptop

# Iterate through the rows in the CSV and create RDF triples
for index, row in df.iterrows():
    laptop_uri = ex[f"Laptop_{row['id']}"]
    g.add((laptop_uri, RDF.type, laptop_type))
    
    # Add other properties as triples
    for column, value in row.items():
        if pd.notna(value):  # Skip NaN values
            property_uri = ex[column]

            # Handle numeric values with appropriate datatypes
            if column in ['weight', 'screen_size', 'graphic_card_size', 'clock_speed']:
                value_literal = Literal(value, datatype=XSD.float)
            else:
                value_literal = Literal(value)

            g.add((laptop_uri, property_uri, value_literal))

# Serialize the RDF graph to Turtle format and save it to a file
output_file = "data2.ttl"
g.serialize(output_file, format="turtle")

print(f"RDF data has been saved to {output_file}")