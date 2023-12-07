# SmartLapRec: Semantic Recommendation System for Laptops

# Description
Our project focuses on developing an expert recommendation system for laptops using Semantic Web technologies. Leveraging RDF and OWL, the system represents laptop specifications, user preferences, and budget constraints. Through SPARQL queries and semantic reasoning, the system dynamically generates personalized recommendations, providing users with tailored suggestions based on their unique preferences and requirements.​

### Acknowledgment

This project is developed as part of CPSC 583 - Expert System Design Theory, where we delved into the principles of building intelligent systems. It serves as a practical implementation of the knowledge gained in the course.

Feel free to explore the project, provide feedback, and tailor it to your specific needs. Happy coding!

## Key Components

1. **Ontology Definition**: The project starts by defining an ontology using RDF and OWL. This ontology captures the essential aspects of laptop specifications and user preferences.

2. **RDF Data Representation**: Laptop data and user profiles are represented in RDF format, incorporating instances of the defined ontology. This structured representation enables the system to understand and process data more effectively.

3. **Semantic Reasoning**: The system is designed to perform semantic reasoning, allowing it to derive additional details and connections about laptops and users. This enhances its ability to provide more accurate and context-aware recommendations.

4. **SPARQL Queries**: SPARQL queries are implemented to retrieve relevant information from the RDF data store. These queries enable the system to generate recommendations based on user-specified criteria, providing a flexible and powerful way to interact with the semantic data.

5. **User Interface**: A user-friendly interface is developed to allow users to input their preferences easily. The system processes these preferences, executes SPARQL queries, and presents personalized recommendations to the users.

## Getting Started

### Prerequisites

- Python 3.11 stable version

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/semantic-web-laptop-recommendation.git

2. ```bash
   pip install -r requirements.txt

3. Run the following command to convert laptop data from a CSV file to RDF triples:

   ```bash
   python3 process_csv_data.py

4. Run the application:

   ```bash
   python3 dashboard.py

5. To load the RDF graph from ontology and data files, convert it to a Networkx graph, and visualize it using Matplotlib:

   ```bash
   python3 graph.py

## Facing any issues???
Feel free to [open an issue](https://github.com/YTushar18/SmartLapRec/issues/new?assignees=&labels=Query&title=Query). We'll be glad to help you.❤️

## Developers
1. [Dhruti Patel](https://github.com/iamdhrutipatel)
2. [Tushar Yadav](https://github.com/YTushar18)
3. [Pratistha Soni](https://github.com/pratishthasoni)