# **E-commerce Query, Product Search, and Chatbot App**

A unified platform for customers to track orders, search for relevant products, and interact with a Product Question-Answering Chatbot. Built with **Streamlit** for an intuitive and interactive user interface.

---

## **Features**

### 1. **Order Status Tracking**
- Enter an Order ID to fetch the current status of an order.
- Displays details such as order ID and status.
  
### 2. **Product Search**
- Input a query to find the most relevant product in the catalog.
- Provides detailed information about the product, including:
  - Name
  - Price
  - Availability
  - Total sales
  - Ratings
  - Current offers

### 3. **Product Chatbot**
- Ask questions about products in natural language.
- Powered by **ProductRAGChatbot**, using embeddings and vector search for accurate and relevant answers.

---

## **Technologies Used**
- **Python**: Backend development and data processing.
- **Streamlit**: For building the user interface.
- **SentenceTransformer**: Embedding generation for product similarity search.
- **PyTorch**: Machine learning framework for chatbot implementation.

---

## **Setup and Installation**

### **Prerequisites**
1. Python 3.8 or above installed on your system.
2. Install virtual environment tool (optional but recommended).

### **Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/shivam92211/EcommerceChatbot.git
   cd ecommerce-app
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate  # For Linux/macOS
   env\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run main.py
   ```

5. Access the app in your browser at `http://localhost:8501`.

---

## **File Structure**
```plaintext
EcommerceChatbot/
├── utils/
│   ├── order.py              # Functions for order tracking
│   ├── product_search.py     # Functions for product search
│   ├── chatbot.py            # Chatbot implementation
├── main.py                   # Entry point for the Streamlit app
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## **Usage**

### 1. **Order Tracking**
- Click on "Order Status Tracking" in the app.
- Enter your order ID and click "Track Order" to fetch the order details.

### 2. **Product Query**
- Click on "Product Query" in the app.
- Enter a query like "Affordable smartphones" or "Best laptops under $1000."
- View detailed information about the most relevant product.

### 3. **Product Chatbot**
- Click on "Product Chatbot" in the app.
- Enter a question, such as "What are the features of iPhone 14?" or "Does this product have a warranty?"
- Get a response from the chatbot powered by the RAG model.

---

## **Customization**

### **Adding New Features**
- To add a new feature:
  - Create a new function in the `utils/` directory.
  - Modify `main.py` to include the feature in navigation.

### **Integrating New Models**
- Update `chatbot.py` to use a different model for generating responses.
- Modify `product_search.py` for alternate similarity search methods.

---

## **Future Enhancements**
1. Add user authentication for a personalized experience.
2. Enable database integration for order tracking and product catalog.
3. Deploy the app on cloud platforms like AWS or Heroku.
4. Introduce voice-enabled queries for the chatbot.

---

## **Contributing**
Contributions are welcome! Please fork the repository and submit a pull request for any features, bug fixes, or improvements.

---

## **License**
This project is licensed under the [MIT License](LICENSE).

