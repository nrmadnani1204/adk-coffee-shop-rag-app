import json 
from google.adk.agents import LlmAgent
from google.adk.apps import App 
from google.cloud import firestore
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.vector import Vector 
from google import genai 

# def get_menu() -> str:
#     """
#     Retrieves the coffee shop menu from the menu.json 

#     Returns: 
#         str: A JSON string representation of the menu items list

#     """
#     try:
#         with open("menu.json", "r") as f:
#             menu_data = json.load(f)
#             return json.dumps(menu_data)
#     except Exception as e:
#         return json.dumps({"Error": f"Could not retrieve menu: {str(e)}"})

def get_menu(query:str) -> str:
    """
    Retrieves coffee shop menu items matching the user query
    Args:
        query: The string search query or preference to find matching menu items. 
    
    Returns: 
        str: A JSON string representing the list of top matching menu items.
    """
    try:
        # initialize clients 
        db = firestore.Client(database="coffee-menu")
        client = genai.Client()

        # Generate embedding for the search query
        response = client.models.embed_content(
            model="text-embedding-004",
            contents=query
        )
        query_vector = response.embeddings[0].values 
        results = db.collection("menu").find_nearest(
            vector_field="embedding",
            query_vector=Vector(query_vector),
            distance_measure=DistanceMeasure.COSINE,
            limit=3
        ).stream()
        menu_data = []
        for doc in results:
            item = doc.to_dict()
            # Remove embedding field to save tokens
            item.pop("embedding", None)
            menu_data.append(item)
        
        return json.dumps(menu_data)

    except Exception as e:
        return json.dumps({"error": f"Could not retrieve the menu {str(e)}"})

barista_agent = LlmAgent(
    name="barista_agent",
    model="gemini-3.5-flash",
    instruction="""
    You are a friendly barista at ☕ Coffee Shop.
Your job is to recommend drinks and pastries to customers based on their preferences.

Rules you MUST follow:
1.  You must recommend items ONLY from the menu returned by get_menu().
2.  Do NOT recommend or suggest any item that is not present in the menu.
3.  If a user's preference is vague or unclear, ask exactly ONE friendly clarifying question to narrow down what they want (e.g., cold or hot, sweet or strong, coffee or pastry).
4.  Be warm and welcoming, but remain professional.
5.  Ground your recommendations in the actual tags, descriptions, and allergens listed in the menu (e.g., if a user is dairy-free, recommend ONLY items tagged 'dairy-free' or with no dairy allergens).
    """,
    tools=[get_menu]
)

app = App(
    name="coffee_barista_app",
    root_agent=barista_agent
)