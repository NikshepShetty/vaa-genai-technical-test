# VAA GenAI Technical Test — RAG Help Assistant

Welcome to the technical assessment for an AI Software Developer role at VAA.  
This test is designed to evaluate your Python, FastAPI, RAG implementation, and prompt engineering skills using OpenAI's API and provided help content.

---

## 🧠 Objective

Build a **RAG-based Help Assistant** that answers customer support queries using retrieved context from our help documentation.  
Use FastAPI, embeddings, a vector store, and OpenAI's GPT model to provide accurate, context-aware responses based on the provided help content.

---

## 📌 Requirements

- Python 3.10+
- FastAPI
- OpenAI API Key
- Pydantic
- Vector store (ChromaDB, FAISS, or similar)
- Embedding model (OpenAI embeddings or sentence-transformers)
- Help content data (provided in `app/seed_data/help_content.json`)

---

## 📋 Rules

You must adhere to the following conditions:

- **Original Work**: The code must be your own work. If you have a strong case to use a small code snippet from someone else's work (e.g., a boilerplate function), it must be clearly commented and attributed to the original author.

- **Testing**: You must include any unit tests you think are appropriate. Consider testing your API endpoints, data processing logic, and OpenAI integration.

- **Evaluations**: Implement evaluation methods to assess your AI responses. Consider testing for accuracy, relevance, proper use of seed data (vs hallucination), response consistency, and guardrail effectiveness.

- **Performance & Quality**: Give consideration to performance, security, and code quality. Your implementation should be production-ready.

- **Code Standards**: Code must be clear, concise, and human readable. Simplicity is often key. We want to see your problem-solving approach and clean architecture.

- **Focus on Implementation**: This is a test of your backend development and AI integration skills. We want to see what you can create with the core technologies. We suggest you spend 4 to 8 hours on the test but the actual amount of time is down to you.

---

## ✅ Your Task

Build a simple RAG ingestion and pipeline with these steps:

### 1. **Ingest Help Content**
- Load `app/seed_data/help_content.json`
- Implement chunking (choose chunk size and overlap)
- Generate embeddings for each chunk

### 2. **Vector Store & Retrieval**
- Initialize a vector store (your choice)
- Store embeddings with source metadata
- Implement similarity search and return top-k chunks

### 3. **Help Q&A API**
- Add an endpoint that retrieves context and answers questions
- Ground answers in retrieved content; include cited sources
- Implement basic guardrails and fallback when no context found

**Bonus (optional but encouraged):**
- Add evaluations (e.g., accuracy, groundedness, citation correctness)
- Add simple caching and/or re-ranking
- Add unit tests for ingestion, retrieval, and API

### Example Request

```json
POST /help-assistant
Content-Type: application/json

{
  "query": "What is the excess baggage policy and fees?"
}

```

---

## 📤 Supplying Your Code

Please create and commit your code into a **public GitHub repository** and supply the link to the recruiter for review.

Thanks for your time, we look forward to hearing from you!
