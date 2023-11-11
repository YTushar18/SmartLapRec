from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery


# Load ontology and data
g = Graph()
g.parse("ontology.ttl", format="turtle")
g.parse("data.ttl", format="turtle")
g.parse("users.ttl", format="turtle")

# User ID (replace this with the actual user ID)
user_id = "ex:User2"

# SPARQL query to get laptop recommendations based on user preferences
query_str = f"""
    SELECT ?laptop
    WHERE {{
        {user_id} a ex:User ;
            ex:prefersProcessor ?processor ;
            ex:prefersRAM ?ram ;
            ex:prefersStorage ?storage ;
            ex:prefersCategory ?category ;
            ex:hasBudget ?budget .

        ?laptop a ex:Laptop ;
            ex:hasProcessor ?processor ;
            ex:hasRAM ?ram ;
            ex:hasStorage ?storage ;
            ex:belongsToCategory ?category ;
            ex:hasPrice ?price .
        
        FILTER (?price <= ?budget)
    }}
"""
query = prepareQuery(query_str, initNs={"ex": "http://example.org/"})
results = g.query(query)

for row in results:
    print(row[0])
