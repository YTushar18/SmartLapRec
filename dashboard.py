import tkinter as tk
from tkinter import scrolledtext
from rdflib.plugins.sparql import prepareQuery
from rdflib import Graph, Literal, Namespace, RDF, URIRef

# Create a namespace for the project
ns1 = Namespace("http://example.org/")

def recommend_laptops():
    print(123)
    # Retrieve user preferences from the entry fields
    user_laptop_type_preference = selected_laptop_type.get()
    budget_preference = budget_entry.get()
    username = username_entry.get()

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

    print("username:",username)
    print("user_laptop_type_preference:",user_laptop_type_preference)
    print("budget_preference:",budget_preference)

    if user_laptop_type_preference == "Gaming":
        query_str = f"""
                    SELECT ?price ?brand ?model
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

                        FILTER (?ram >= 8 && ?storage >= 500 && ?screen > 15 && ?gc_size >= 2 &&
                                ?price <= {budget_preference} && 
                                ((regex(str(?processor), "intel") &&
                                (regex(str(?processor_model), "i5") || 
                                regex(str(?processor_model), "i3") || 
                                regex(str(?processor_model), "i7"))) || 
                                regex(str(?processor), "amd")) &&
                                regex(str(?os), "windows"))
                    }}
                    """
    elif user_laptop_type_preference == "Development":
        query_str = f"""
                    SELECT ?price ?brand ?model
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

                        FILTER (?ram >= 2 && ?storage >= 128 && ?screen > 12 &&
                                ?price <= {budget_preference} && 
                                regex(str(?processor), "intel") && 
                                regex(str(?os), "windows"))
                    }}
                    """
    elif user_laptop_type_preference == "Home":
        query_str = f"""
                    SELECT ?price ?brand ?model
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
                    SELECT ?price ?brand ?model
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

    for row in results:
        print('....',row.price, row.brand, row.model)
    
    # Display the recommendations in the text box
    recommendations_text.delete(1.0, tk.END)  # Clear previous content
    recommendations_text.insert(tk.END,f"Hi {username}, we have {len(results)} recomendations for you....\n")
    for ind, row in enumerate(results):
        recommendations_text.insert(tk.END, "\n")
        recommendations_text.insert(tk.END, f"{ind+1}. {row.brand} {row.model}\n")
        recommendations_text.insert(tk.END, f"    Cost: {row.price}/- inr\n")




import tkinter as tk

def get_screen_dimensions(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return screen_width, screen_height

root = tk.Tk()
root.title("Laptop Recommendation System")

# Set the dimensions of the main window
window_width = 800
window_height = 600
screen_width, screen_height = get_screen_dimensions(root)
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create and place entry fields for user preferences

# Username label and entry
username_label = tk.Label(root, text="Username:", font=("Arial", 25))
username_label.grid(row=0, column=0, sticky="w")

username_entry = tk.Entry(root, font=("Arial", 25))
username_entry.grid(row=0, column=1, columnspan=2, sticky="w")

# Dropdown menu for laptop type preference
laptop_types = ["Gaming", "Development", "Home"]
label_font = ("Arial", 25)  # Adjust the font size and family as needed

laptop_type_preference_label = tk.Label(root, text="Laptop Category:", font=label_font)
laptop_type_preference_label.grid(row=1, column=0, sticky="w", pady=5)

# Use tk.StringVar to store the selected value
selected_laptop_type = tk.StringVar(root)
selected_laptop_type.set(laptop_types[0])  # Set the default value

# Determine the width and height of the dropdown menu dynamically
dropdown_width = window_width // 15  # You can adjust the factor as needed
dropdown_height = 1  # Set the desired height

# Create the dropdown menu with the determined width, height, and font
dropdown_font = ("Arial", 25)  # Adjust the font size and family as needed
laptop_type_dropdown = tk.OptionMenu(root, selected_laptop_type, *laptop_types)
laptop_type_dropdown.config(width=17, height=dropdown_height, font=dropdown_font)
laptop_type_dropdown.grid(row=1, column=1, columnspan=2, sticky="w")  # Spanning 2 columns, aligned to the west

# Budget label with specified width and height
budget_label = tk.Label(root, text="Budget(upper bound in inr):", font=label_font, height=2)  # Set the desired height
budget_label.grid(row=2, column=0, sticky="w")

# Budget entry with the same width as the dropdown menu
budget_entry = tk.Entry(root, font=("Arial", 25))
# budget_entry.config(width=30)
budget_entry.grid(row=2, column=1, columnspan=2, sticky="w")  # Spanning 2 columns, aligned to the west

# Adjust column weights to control width
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.columnconfigure(2, weight=2)

# Create a button to trigger recommendations
recommend_button_font = ("Arial", 24, "bold")  # Adjust the font size and style as needed
recommend_button = tk.Button(root, text="Get Recommendations", font=recommend_button_font, command=recommend_laptops)
recommend_button.grid(row=3, column=0, columnspan=2, pady=10)  # Spanning 3 columns, with some vertical padding

# Create a text box with the same dimensions as the dropdown menu
recommendations_text_font = ("Arial", 24)  # Adjust the font size and family as needed
recommendations_text = scrolledtext.ScrolledText(root, width=dropdown_width, height=dropdown_height+12, wrap=tk.WORD, font=recommendations_text_font)
recommendations_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)  # Spanning 2 columns, with some horizontal and vertical padding

# Start the Tkinter event loop
root.mainloop()
