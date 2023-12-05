import tkinter as tk
from tkinter import scrolledtext
from rdflib.plugins.sparql import prepareQuery
from rdflib import Graph, Literal, Namespace, RDF, URIRef

# Create a namespace for the project
ex = Namespace("http://example.org/")

def recommend_laptops():
    # Retrieve user preferences from the entry fields
    laptop_type_preference = laptop_type_preference.get()
    processor_preference = processor_entry.get()
    ram_preference = ram_entry.get()
    storage_preference = storage_entry.get()
    category_preference = category_entry.get()
    budget_preference = budget_entry.get()

    # Create a new RDF graph and add user preferences
    user_graph = Graph()
    user_uri = URIRef(f"http://example.org/User1")  # You can use a dynamic user ID
    user_graph.add((user_uri, RDF.type, ex.User))
    user_graph.add((user_uri, ex.prefersProcessor, Literal(processor_preference)))
    user_graph.add((user_uri, ex.prefersRAM, Literal(ram_preference)))
    user_graph.add((user_uri, ex.prefersStorage, Literal(storage_preference)))
    user_graph.add((user_uri, ex.prefersCategory, Literal(category_preference)))
    user_graph.add((user_uri, ex.hasBudget, Literal(budget_preference)))

    # Merge user preferences into the main graph
    g = Graph()
    g.parse("ontology.ttl", format="turtle")  # Load ontology
    g.parse("data.ttl", format="turtle")  # Load existing data
    g.parse("users.ttl", format="turtle")  # Load existing user data
    g += user_graph

    # SPARQL query to get laptop recommendations based on user preferences
    query_str = f"""
        SELECT ?laptop
        WHERE {{
            {user_uri} a ex:User ;
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

    query = prepareQuery(query_str, initNs={"ex": ex})
    results = g.query(query)

    # Print or use the recommendations as needed (for demonstration purposes)
    for row in results:
        print(row[0])
    
    # Display the recommendations in the text box
    recommendations_text.delete(1.0, tk.END)  # Clear previous content
    for row in results:
        recommendations_text.insert(tk.END, f"{row[0]}\n")

# Create the main window
root = tk.Tk()
root.title("Apple Laptop Recommendation System")

# Create and place entry fields for user preferences

laptop_type_preference_label = tk.Label(root, text="Type (gaming/clerk/home):")
laptop_type_preference_label.grid(row=0, column=0, sticky="e")
laptop_type_preference = tk.Entry(root)
laptop_type_preference.grid(row=0, column=1)

# processor_label = tk.Label(root, text="Processor:")
# processor_label.grid(row=1, column=0, sticky="e")
# processor_entry = tk.Entry(root)
# processor_entry.grid(row=1, column=1)

# ram_label = tk.Label(root, text="RAM:")
# ram_label.grid(row=2, column=0, sticky="e")
# ram_entry = tk.Entry(root)
# ram_entry.grid(row=2, column=1)

# storage_label = tk.Label(root, text="Storage:")
# storage_label.grid(row=3, column=0, sticky="e")
# storage_entry = tk.Entry(root)
# storage_entry.grid(row=3, column=1)

# category_label = tk.Label(root, text="Category:")
# category_label.grid(row=4, column=0, sticky="e")
# category_entry = tk.Entry(root)
# category_entry.grid(row=4, column=1)

budget_label = tk.Label(root, text="Budget(upper bound):")
budget_label.grid(row=5, column=0, sticky="e")
budget_entry = tk.Entry(root)
budget_entry.grid(row=5, column=1)


# Create a button to trigger recommendations
recommend_button = tk.Button(root, text="Get Recommendations", command=recommend_laptops)
recommend_button.grid(row=7, column=0, columnspan=2)


# Create a text box to display recommendations
recommendations_text = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
recommendations_text.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
