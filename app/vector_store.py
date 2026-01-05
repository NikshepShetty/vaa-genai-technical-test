"""
Vector Store Service for RAG Implementation

TODO: Implement the following components for the RAG system:

1. Document Processing:
    - Load help content from seed_data/help_content.json
    - Convert records into searchable text chunks (choose chunk size/overlap)
    - Generate embeddings for each chunk

2. Vector Store Setup:
    - Choose and initialize vector database (ChromaDB, FAISS, etc.)
    - Store embeddings with metadata (source id, title, category)
    - Implement similarity search functionality

3. Retrieval Methods:
    - Semantic search based on query embeddings
    - Optional filtering by category
    - Return top-k relevant chunks with scores

Example structure:

class VectorStoreService:
    def __init__(self):
        # Initialize your chosen vector store
        pass
    
    def load_and_process_documents(self, file_path: str):
        # Load help content and create embeddings
        pass
    
    def similarity_search(self, query: str, top_k: int = 3) -> list[dict]:
        # Perform semantic search and return relevant context
        pass
    
    def add_document(self, content: str, metadata: dict):
        # Add new document to vector store
        pass
"""

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import os
from dotenv import load_dotenv
from app.data import help_content

load_dotenv()

class VectorStoreService:
    """
    Placeholder for RAG vector store implementation.
    
    Candidates should implement this class with their chosen vector database.

    Chosen Vector DB - Chroma
    """
    
    def __init__(self):
        # TODO: Initialize vector store (ChromaDB, FAISS, etc.)
        # Get OpenAi key from .env file
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("No OpenAI key set. Enter key into .env file")
        
        # Category set for validation later
        self._categories: set[str] = set()

        # Optional reranker
        self._reranker = None # reranker model
        self.use_reranker: bool = False # reranker switch

        self.client = chromadb.PersistentClient(path="./chroma_data")
        self.collection = self.client.get_or_create_collection(
            name="help_content",
            embedding_function=OpenAIEmbeddingFunction(
                model_name="text-embedding-3-small",
                api_key=api_key
            ),
            # Chroma defaults to squared L2 distance, switching to cosine distances (which is 1 - cosine similarity in chroma, so lower is better)
            configuration={
                "hnsw": {"space": "cosine"} 
            }
            )
    
    def load_help_content(self):
        """Load and process help content into vector store."""
        # TODO: Load from app/seed_data/help_content.json

        # Help content has a small amount of json data and the content isn't long enough for chunking to make sense. 
        # So, 1 json entry = 1 chunk right now

        # Modifying shape of data to fit chromadb's collection requirements
        ids: list[str] = []
        documents: list[str] = []
        metadatas: list[dict[str, str]] = []

        for entry in help_content:
            source_id = str(entry["id"]).strip()
            title = str(entry["title"]).strip()
            category = str(entry["category"]).strip().lower() # Keeping all category values lowercase
            self._categories.add(category)
            content = str(entry["content"]).strip()

            documents.append(f"{title}\n\n{content}") # Text/documents will be title + content
            ids.append(source_id)

            # ID is included in metadata as well in case chunking strategy changes later
            metadatas.append(
                {
                    "source_id": source_id,
                    "title": title,
                    "category": category
                }
            )

        if not ids:
            return None
        
        # Upsert in chroma will add new entries if ID is new and update if ID already exists
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        # TODO: Implement chunking with overlap; embed and persist with source IDs
        # Not required with such small chunks, will only add complications without add any benefits
        # If chunking is necessary or if the documents get long, we could use the RecursiveCharacterTextSplitter function from langchain.
        return None


    # Reranker is switched off currently due to having very little improvement for the RAGAS metrics. Could be tested later with larger dataset
    def rerank_results(self, query: str, results: list[dict[str, object]]) -> list[dict[str, object]]:
        """Rerank retrieved results using a cross-encoder model."""
        from sentence_transformers import CrossEncoder

        if not results:
            return results
        
        if self._reranker is None:
            self._reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        
        pairs = [(query, entry["text"]) for entry in results]
        scores = self._reranker.predict(pairs)

        scored_results: list[tuple[dict[str, object], float]] = []
        for result, score in zip(results, scores):
            scored_results.append((result, float(score)))

        # Sort results by reranker score (higher is better)
        scored_results.sort(key=lambda item: item[1], reverse=True)

        # Return in original shape
        reranked_results: list[dict[str, object]] = []
        for result, _ in scored_results:
            reranked_results.append(dict(result))
            
        return reranked_results
    
    def search(self, query: str, top_k: int = 3, category: str | None = None) -> list[dict[str, object]]:
        """Search for relevant context based on user query."""
        # TODO: Convert query to embedding and perform similarity search

        result = self.collection.query(
            query_texts=[query],
            n_results=min(max(1, top_k), 50), # Setting the range of top_k between 1 and 50
            include=["documents", "distances","metadatas"],
            where={"category": {"$eq": category.strip().lower()}} if category is not None else None # If category is passed, filter based on category
        )

        # Early check for empty result
        if len(result["documents"][0])==0:
            return []

        # Convert Chroma query shape (Dict[str, List[List[str]]]) into requested output shape
        formatted_result: list[dict[str, object]] = []

        # Return list of {text: str, source_id: str, score: float}
        for doc, meta, dist in zip(result["documents"][0], result["metadatas"][0], result["distances"][0]):
            # Convert from cosine distance to cosine similarity (higher is more similar)
            cosine_sim = 1-float(dist)
            formatted_result.append(
                {
                    "text": doc,
                    "source_id": meta["source_id"],
                    "score": cosine_sim if cosine_sim>0 else 0 # Cosine has a range from -1 to 1, setting anything below 0 to 0.
                }
            )
        if self.use_reranker:
            formatted_result = self.rerank_results(query, formatted_result)

        return formatted_result
    
    def get_category_list(self) -> list[str]:
        """Return allowed categories for validation"""
        return sorted(self._categories)