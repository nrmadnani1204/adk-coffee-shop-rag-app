import json 
import os
from google import genai
from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector 


db = firestore.Client(database="coffee-menu")
client = genai.Client(
    vertexai=True,
    project=os.environ.get("PROJECT_ID"),
    location=os.environ.get("REGION", "us-central1")
)

with open("menu.json", "r") as f:
    menu_items = json.load(f)

for item in menu_items:
    # name as document id
    doc_id = item.get("name","").lower().replace(" ","-")

    # generate embedding vector
    text_to_embed = f"{item['name']}: {item['description']}"
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=text_to_embed
    )
    embedding = response.embeddings[0].values
    # Add embedding vector to the menu item data
    item["embedding"] = Vector(embedding)

    # add item to table menu
    db.collection("menu").document(doc_id).set(item)


print("Added json with vector embeddings to Firestore successfully!!!")

