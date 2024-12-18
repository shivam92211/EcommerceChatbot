import streamlit as st
from utils.order import get_order_status
from utils.product_search import find_most_similar_product
from utils.chatbot import ProductRAGChatbot

# ---------------------- Streamlit UI ---------------------- #
st.title("E-commerce Query, Product Search, and Chatbot App")
st.write("A unified platform for order tracking, product search, and a product Q&A chatbot.")

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Vertical button navigation
if st.button("Order Status Tracking"):
    st.session_state.page = "Order Status Tracking"
if st.button("Product Query"):
    st.session_state.page = "Product Query"
if st.button("Product Chatbot"):
    st.session_state.page = "Product Chatbot"

# ---------------------- Order Status Tracking ---------------------- #
if st.session_state.page == "Order Status Tracking":
    st.header("Track Order Status")
    order_id = st.text_input("Enter Order ID", "")
    if st.button("Track Order"):
        if order_id:
            result = get_order_status(order_id)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"Order ID: {result['order_id']}\nStatus: {result['status']}")
        else:
            st.warning("Please enter a valid Order ID.")

# ---------------------- Product Query ---------------------- #
elif st.session_state.page == "Product Query":
    st.header("Find Most Relevant Product")
    query = st.text_input("Enter your query about a product", "")
    
    if st.button("Search Product"):
        if query:
            st.info("Searching for the most relevant product...")
            product, error = find_most_similar_product(query)
            if error:
                st.error(error)
            else:
                st.success("Here is the most similar product:")
                st.write(f"**Product Name:** {product.get('name', 'Unknown')}")
                st.write(f"**Price:** ${product.get('price', 'Unknown')}")
                st.write(f"**Quantity Left:** {product.get('quantity_left', 'Unknown')}")
                st.write(f"**Total Sold:** {product.get('total_sold', 'Unknown')}")
                st.write(f"**Rating:** {product.get('rating', 'Unknown')}/5")
                st.write(f"**Offer:** {product.get('offer', 'Unknown')}")
        else:
            st.warning("Please enter a query to search for products.")

# ---------------------- Product Chatbot ---------------------- #
elif st.session_state.page == "Product Chatbot":
    st.header("Product RAG Chatbot")
    st.write("Ask questions about our products!")

    # Initialize the chatbot instance only once
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = ProductRAGChatbot()
        st.success("Chatbot initialized with embeddings and vector store.")

    # Access the chatbot instance from session state
    chatbot = st.session_state.chatbot

    # Initialize chat history if not already present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # User input
    user_input = st.text_input("You:", key="user_input")
    if st.button("Send"):
        if user_input:
            with st.spinner("Generating response..."):
                response = chatbot.generate_response(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", response))

    # Display chat history with unique keys
    for i, (user, bot) in enumerate(st.session_state.chat_history):
        st.text_area(label=f"{user}:", value=bot, height=100, key=f"chat_{i}")
