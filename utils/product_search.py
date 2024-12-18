from sklearn.metrics.pairwise import cosine_similarity
from utils.config import embedding_model, products_collection

def find_most_similar_product(query: str):
    """Find the most similar product based on the query."""
    # Generate embedding for query
    query_embedding = embedding_model.encode(query).tolist()

    # Fetch all products with embeddings
    documents_with_embeddings = list(products_collection.find({"embedding": {"$exists": True}}))

    # Compute similarities
    similarities = []
    for doc in documents_with_embeddings:
        similarity = cosine_similarity([query_embedding], [doc["embedding"]])[0][0]
        similarities.append((doc, similarity))

    # Sort by similarity
    if similarities:
        similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
        return similarities[0][0], None  # Return the most similar document
    else:
        return None, "No products found with embeddings."
