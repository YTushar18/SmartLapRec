import tkinter as tk
from tkinter import scrolledtext
from rdflib.plugins.sparql import prepareQuery
from rdflib import Graph, Literal, Namespace, RDF, URIRef

# Create a namespace for the project
ex = Namespace("http://example.org/")

def recommend_laptops():
    # Retrieve user preferences from the entry fields
    laptop_type_preference = laptop_type_preference.get()
    print(laptop_type_preference)
    budget_preference = budget_entry.get()

    # Create a new RDF graph and add user preferences
    user_graph = Graph()
    user_uri = URIRef(f"http://example.org/User1")  # You can use a dynamic user ID
    user_graph.add((user_uri, RDF.type, ex.User))
    user_graph.add((user_uri, ex.hasBudget, Literal(budget_preference)))

    # Merge user preferences into the main graph
    g = Graph()
    g.parse("ontology.ttl", format="turtle")  # Load ontology
    g.parse("data.ttl", format="turtle")  # Load existing data
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



import tkinter as tk

def get_screen_dimensions(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return screen_width, screen_height

root = tk.Tk()
root.title("Apple Laptop Recommendation System")

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
username_label.grid(row=0, column=0, sticky="e")

username_entry = tk.Entry(root, font=("Arial", 25))
username_entry.grid(row=0, column=1, columnspan=2, sticky="w")


# Dropdown menu for laptop type preference
laptop_types = ["Gaming", "Clerk", "Home"]
label_font = ("Arial", 25)  # Adjust the font size and family as needed

laptop_type_preference_label = tk.Label(root, text="Type:", font=label_font)
laptop_type_preference_label.grid(row=1, column=0, sticky="e")

# Use tk.StringVar to store the selected value
selected_laptop_type = tk.StringVar(root)
selected_laptop_type.set(laptop_types[0])  # Set the default value

# Determine the width and height of the dropdown menu dynamically
dropdown_width = window_width // 15  # You can adjust the factor as needed
dropdown_height = 1  # Set the desired height

# Create the dropdown menu with the determined width, height, and font
dropdown_font = ("Arial", 25)  # Adjust the font size and family as needed
laptop_type_dropdown = tk.OptionMenu(root, selected_laptop_type, *laptop_types)
laptop_type_dropdown.config(width=dropdown_width, height=dropdown_height, font=dropdown_font)
laptop_type_dropdown.grid(row=1, column=1, columnspan=2, sticky="w")  # Spanning 2 columns, aligned to the west

# Budget label with specified height
budget_label = tk.Label(root, text="Budget(upper bound):", font=label_font, height=2)  # Set the desired height
budget_label.grid(row=2, column=0, sticky="e")

# Budget entry with the same width as the dropdown menu
budget_entry = tk.Entry(root, width=dropdown_width)
budget_entry.grid(row=2, column=1, columnspan=2, sticky="w")  # Spanning 2 columns, aligned to the west

# Create a button to trigger recommendations
recommend_button_font = ("Arial", 24, "bold")  # Adjust the font size and style as needed
recommend_button = tk.Button(root, text="Get Recommendations", font=recommend_button_font)
recommend_button.grid(row=3, column=0, columnspan=2, pady=10)  # Spanning 3 columns, with some vertical padding

# Create a text box with the same dimensions as the dropdown menu
recommendations_text_font = ("Arial", 24)  # Adjust the font size and family as needed
recommendations_text = tk.Text(root, width=dropdown_width, height=dropdown_height+4, wrap=tk.WORD, font=recommendations_text_font)
recommendations_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)  # Spanning 3 columns, with some horizontal and vertical padding


recommendations_text_font = ("Arial", 24)  # Adjust the font size and family as needed
recommendations_text = scrolledtext.ScrolledText(root, width=dropdown_width, height=dropdown_height+12, wrap=tk.WORD, font=recommendations_text_font)
recommendations_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)  # Spanning 2 columns, with some horizontal and vertical padding

# Start the Tkinter event loop
root.mainloop()

# import tkinter as tk

# def get_screen_dimensions(root):
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     return screen_width, screen_height

# def recommend_laptops():
#     # Retrieve user preferences from the entry fields
#     username = username_entry.get()
#     laptop_type_preference = selected_laptop_type.get()
#     budget_preference = budget_entry.get()

#     # Your existing code for recommendations (replace with actual logic)

#     # Display the recommendations in the text box
#     recommendations_text.delete(1.0, tk.END)  # Clear previous content
#     recommendations_text.insert(tk.END, "Your recommendations go here.\n")

# root = tk.Tk()
# root.title("Apple Laptop Recommendation System")

# window_width = 800
# window_height = 600
# screen_width, screen_height = get_screen_dimensions(root)
# x_position = (screen_width - window_width) // 2
# y_position = (screen_height - window_height) // 2

# root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# # Username label and entry
# username_label = tk.Label(root, text="Username:", font=("Arial", 25))
# username_label.grid(row=0, column=3, sticky="e")

# username_entry = tk.Entry(root, font=("Arial", 25))
# username_entry.grid(row=0, column=4, columnspan=2, sticky="w")

# # Your existing code for laptop type preference, budget, button, and text box

# # Create a button to trigger recommendations
# recommend_button_font = ("Arial", 24, "bold")
# recommend_button = tk.Button(root, text="Get Recommendations", font=recommend_button_font, command=recommend_laptops)
# recommend_button.grid(row=2, column=3, columnspan=3, pady=10)

# # Create a text box with the same dimensions as the dropdown menu
# recommendations_text_font = ("Arial", 24)
# recommendations_text = tk.Text(root, width=dropdown_width, height=dropdown_height+4, wrap=tk.WORD, font=recommendations_text_font)
# recommendations_text.grid(row=3, column=3, columnspan=2, padx=10, pady=10)

# root.mainloop()
