import streamlit as st
import json 


st.set_page_config(
    page_title="Coffee Shop - Barista Bot",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    div[data-testid="element-container"]:has(.header-container),
    div.element-container:has(.header-container) {
        position: sticky;
        top: 2.875rem;
        z-index: 999;
        background-color: transparent;
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("""
<div class="header-container" style="text-align: center; padding: 20px; background: linear-gradient(135deg, #8B5E3C, #6F4E37); color: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700; color: white;">☕ ☕ Coffee Shop</h1>
    <p style="margin: 5px 0 0 0; font-size: 1.1rem; opacity: 0.9; color: white;">Your friendly AI Barista is ready to help you find the perfect drink or pastry!</p>
</div>
""", unsafe_allow_html=True)

try:
    with open("menu.json", "r") as f:
        menu_items = json.load(f)
except Exception as e:
    st.error(f"Error loading menu list {str(e)}")
    menu_items = []


with st.sidebar:
    st.markdown("## Coffee Shop Menu")
    st.markdown("Explore our offering and ask the barista for recommendations")
    st.markdown("---")

    for item in menu_items:
        with st.container(border=True):
            st.markdown(f"**{item['name']}**  .  **${item['price']}**")
            st.caption(item['description'])

            # badges for tags and allergens
            tags = " ".join([f" `{t}`" for t in item.get('tags',[])])
            if tags:
                st.markdown(tags)
            allergens = ", ".join(item.get("allergens", []))
            if allergens:
                st.markdown(f"Warning! Note Allergens: {allergens}")


# Chat interface
if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())

if "runner" not in st.session_state:
    from google.adk.runners import InMemoryRunner
    from agent import app
    st.session_state.runner = InMemoryRunner(app=app)

if "messages" not in st.session_state:
    st.session_state.messages  = [
        {"role": "assistant", 
        "content": "Welcome to Barista Coffee Shop! What can I get started for you today?"}
    ]

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# User Input
if prompt := st.chat_input("Ask for recommendations (e.g., 'What dairy free pastries do you have?')"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    with st.chat_message("assistant"):
        try:
            import asyncio 

            async def fetch_response():
                return await st.session_state.runner.run_debug(
                    prompt,
                    session_id=st.session_state.session_id
                )

            res_events = asyncio.run(fetch_response())

            response_text = "".join(
                [
                part.text 
                for event in res_events 
                if event.content and event.content.parts
                for part in event.content.parts 
                if part.text
                ]
            )

            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        
        except Exception as e:
            st.error(f"Error in generating response: {str(e)}")
        
    

