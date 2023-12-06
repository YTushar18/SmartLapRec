import tkinter as tk
from tkinter import scrolledtext
from rdflib.plugins.sparql import prepareQuery
from rdflib import Graph, Literal, Namespace, RDF, URIRef

# Create a namespace for the project
ns1 = Namespace("http://example.org/")


def recommend_laptops():
    # Retrieve user preferences from the entry fields
    user_laptop_type_preference = str(laptop_type_preference.get())
    budget_preference = int(budget_entry.get())  # Assuming this is a string input

    # Create a new RDF graph and add user preferences
    user_graph = Graph()
    user_uri = URIRef(f"http://example.org/User1")  # You can use a dynamic user ID
    user_graph.add((user_uri, RDF.type, ns1.User))
    user_graph.add(
        (user_uri, ns1.prefersLaptopType, Literal(user_laptop_type_preference))
    )
    user_graph.add((user_uri, ns1.hasBudget, Literal(budget_preference)))

    # Merge user preferences into the main graph
    g = Graph()
    g.parse("ontology.ttl", format="turtle")  # Load ontology
    g.parse("data.ttl", format="turtle")  # Load existing data
    g += user_graph

    if user_laptop_type_preference == "gaming":
        query_str = f"""
                    SELECT ?ram ?brand ?model
                    WHERE {{
                        ?laptop a ns1:Laptop ;
                                ns1:ram ?ram ;
                                ns1:brand ?brand ;
                                ns1:model ?model ;
                                ns1:hd_size ?storage ;
                                ns1:screen_size ?screen ;
                                ns1:graphic_card_size ?gc_size ;
                                ns1:processor_brand ?processor ;
                                ns1:processor_model ?processor_model ;
                                ns1:price ?price ;
                                ns1:os ?os .

                        FILTER (?ram >= 8 && ?storage >= 512 && ?screen > 15 && ?gc_size >= 2 &&
                                ?price <= {budget_preference} && 
                                ((regex(str(?processor), "intel") &&
                                (regex(str(?processor_model), "i5") || 
                                regex(str(?processor_model), "i3") || 
                                regex(str(?processor_model), "i7"))) || 
                                regex(str(?processor), "amd")) &&
                                regex(str(?os), "windows"))
                    }}
                    """
    elif user_laptop_type_preference == "clerk":
        query_str = f"""
                    SELECT ?ram ?brand ?model
                    WHERE {{
                        ?laptop a ns1:Laptop ;
                                ns1:ram ?ram ;
                                ns1:brand ?brand ;
                                ns1:model ?model ;
                                ns1:hd_size ?storage ;
                                ns1:screen_size ?screen ;
                                ns1:processor_brand ?processor ;
                                ns1:os ?os ;
                                ns1:price ?price .

                        FILTER (?ram >= 2 && ?storage >= 512 && ?screen > 12 &&
                                ?price <= {budget_preference} && 
                                regex(str(?processor), "intel") && 
                                regex(str(?os), "windows"))
                    }}
                    """
    elif user_laptop_type_preference == "dev":
        query_str = f"""
                    SELECT ?ram ?brand ?model
                    WHERE {{
                        ?laptop a ns1:Laptop ;
                                ns1:ram ?ram ;
                                ns1:brand ?brand ;
                                ns1:model ?model ;
                                ns1:hd_size ?storage ;
                                ns1:screen_size ?screen ;
                                ns1:clock_speed ?speed ;
                                ns1:graphic_card_size ?gc_size ;
                                ns1:processor_brand ?processor ;
                                ns1:processor_model ?processor_model ;
                                ns1:price ?price ;
                        
                        FILTER (?ram >= 8 && ?storage >= 512 && ?screen > 14 &&
                                ?price <= {budget_preference} && 
                                ?speed >= 2.3 &&
                                ((?processor = "intel" && 
                                (?processor_model = "i5" || ?processor_model = "i3")) &&
                                ?gc_size >= 1))
                        }}
                    """
    else:
        query_str = f"""
                    SELECT ?ram ?brand ?model
                    WHERE {{
                        ?laptop a ns1:Laptop ;
                                ns1:ram ?ram ;
                                ns1:brand ?brand ;
                                ns1:model ?model ;
                                ns1:hd_size ?storage ;
                                ns1:screen_size ?screen ;
                                ns1:processor_brand ?processor ;
                                ns1:os ?os ;
                                ns1:price ?price .

                        FILTER (?ram >= 4 && ?storage >= 512 && ?screen > 13 &&
                                ?price <= {budget_preference} && 
                                (regex(str(?os), "windows") || regex(str(?os), "mac")))
                    }}
                    """

    query = prepareQuery(query_str, initNs={"ns1": ns1})
    results = g.query(query)

    # Print or use the recommendations as needed (for demonstration purposes)
    print(len(results))

    for row in results:
        print("....", row.ram, row.brand, row.model)

    # Display the recommendations in the text box
    recommendations_text.delete(1.0, tk.END)  # Clear previous content
    recommendations_text.insert(tk.END, "Here are the results...\n")
    for row in results:
        recommendations_text.insert(tk.END, f"{row.brand} {row.model}\n")


# Create the main window
root = tk.Tk()
root.title("Apple Laptop Recommendation System")

# Create and place entry fields for user preferences

laptop_type_preference_label = tk.Label(root, text="Type (gaming/clerk/home):")
laptop_type_preference_label.grid(row=0, column=0, sticky="e")
laptop_type_preference = tk.Entry(root)
laptop_type_preference.grid(row=0, column=1)

budget_label = tk.Label(root, text="Budget(upper bound):")
budget_label.grid(row=5, column=0, sticky="e")
budget_entry = tk.Entry(root)
budget_entry.grid(row=5, column=1)

# Create a button to trigger recommendations
recommend_button = tk.Button(
    root, text="Get Recommendations", command=recommend_laptops
)
recommend_button.grid(row=7, column=0, columnspan=2)

# Create a text box to display recommendations
recommendations_text = scrolledtext.ScrolledText(
    root, width=40, height=10, wrap=tk.WORD
)
recommendations_text.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
