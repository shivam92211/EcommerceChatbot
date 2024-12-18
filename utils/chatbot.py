import os
import json
import faiss
import logging
from groq import Groq
import streamlit as st
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

class ProductRAGChatbot:
    def __init__(
        self,
        data_path: Optional[str] = None,
        raw_data: Optional[List[str]] = None,
        model_name: str = "all-MiniLM-L6-v2",
        # api_key: Optional[str] = None,
    ):
        """
        Initialize the RAG Chatbot with product data and embedding model
        """
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Set GROQ_API_KEY environment variable or pass api_key."
            )

        # Load product data
        try:
            if data_path:
                with open(data_path, "r") as f:
                    self.products = json.load(f)
            elif raw_data:
                self.products = self._parse_raw_data(raw_data)
            else:
                with open("product/data.txt", "r") as file:
                    raw_data = file.readlines()
                self.products = self._parse_raw_data(raw_data)
        except Exception as e:
            logger.error(f"Error loading product data: {e}")
            self.products = []

        if not self.products:
            logger.warning("No product data loaded. Chatbot may not function correctly.")

        try:
            self.embedding_model = SentenceTransformer(model_name)
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

        self._prepare_vector_store()
        self.chat_history = []

        try:
            self.client = Groq(api_key=self.api_key)
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            raise

        self.model = "llama3-8b-8192"

    def _parse_raw_data(self, raw_data: List[str]) -> List[Dict[str, Any]]:
        raw_data = [line.strip() for line in raw_data if line.strip()]
        products = []
        for line in raw_data:
            try:
                parts = line.split(", ")
                product_dict = {}
                for part in parts:
                    key, value = part.split(": ")
                    cleaned_key = key.lower().replace(" ", "_")
                    product_dict[cleaned_key] = value
                required_keys = ["product", "price", "rating"]
                if all(key in product_dict for key in required_keys):
                    products.append(product_dict)
                else:
                    logger.warning(f"Skipping invalid product entry: {line}")
            except Exception as e:
                logger.warning(f"Could not parse line '{line}'. Error: {e}")
        return products

    def _prepare_vector_store(self):
        if not self.products:
            logger.warning("No products to create vector store.")
            return
        product_texts = [
            f"{p.get('product', 'Unknown')} with price {p.get('price', 'N/A')} and rating {p.get('rating', 'N/A')}"
            for p in self.products
        ]
        try:
            self.embeddings = self.embedding_model.encode(product_texts)
            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(self.embeddings)
        except Exception as e:
            logger.error(f"Failed to create vector store: {e}")
            self.embeddings = None
            self.index = None

    def retrieve_relevant_products(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if self.index is None:
            logger.warning("Vector index not initialized. Returning all products.")
            return self.products[:top_k]
        query_embedding = self.embedding_model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.products[i] for i in indices[0]]

    def generate_response(self, query: str) -> str:
        relevant_products = self.retrieve_relevant_products(query)
        context = "\n".join(
            [
                f"Product: {p.get('product', 'Unknown')}, "
                f"Price: {p.get('price', 'N/A')}, "
                f"Rating: {p.get('rating', 'N/A')}, "
                f"Offer: {p.get('offer', 'No offer')}"
                for p in relevant_products
            ]
        )
        messages = [
            {
                "role": "system",
                "content": "You are a helpful product assistant. Use the provided context to answer questions about products.",
            },
            {
                "role": "user",
                "content": f"Chat History: {self._format_chat_history()}\n\nContext Products:\n{context}\n\nQuery: {query}",
            },
        ]
        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages, model=self.model
            )
            response = chat_completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            response = f"Sorry, I encountered an error processing your request. {str(e)}"
        self.chat_history.append({"user": query, "bot": response})
        return response

    def _format_chat_history(self, max_history: int = 3) -> str:
        history_str = ""
        for interaction in self.chat_history[-max_history:]:
            history_str += f"User: {interaction['user']}\nBot: {interaction['bot']}\n"
        return history_str

