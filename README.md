# VAA GenAI Technical Test — AI Travel Assistant

Welcome to the technical assessment for an AI Software Developer role at VAA.  
This test is designed to evaluate your Python, FastAPI, RAG implementation, and prompt engineering skills using OpenAI's API and provided help content.

---

## 🧠 Objective

Build a **RAG-based Help Assistant** that answers customer support queries using retrieved context from our help documentation.  
You should use FastAPI, vector embeddings, a vector store, and OpenAI's GPT model to provide accurate, context-aware responses based on the provided help content.

---

## 📌 Requirements

- Python 3.10+
- FastAPI
- OpenAI API Key
- Pydantic
- Vector store (ChromaDB, FAISS, or similar)
- Embedding model (OpenAI embeddings or sentence-transformers)
- Help content data (provided)

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

Build a RAG-based help system with these three core components:

### 1. **Process Help Content**
- Take the provided seed data files (hotels, flights, experiences catalogues)
- Implement chunking strategy for optimal retrieval of travel information
- Generate embeddings for each chunk of travel data

### 2. **Vector Store Implementation**

- Set up a vector database to store embeddings
- Implement similarity search functionality
- Ensure efficient retrieval of relevant context

### 3. **RAG-Enhanced API**
- Update the existing endpoint to use RAG architecture
- Retrieve relevant context from travel catalogues before generating responses
- Combine retrieved context with user queries for accurate travel recommendations
- Implement appropriate guardrails

**Additional Requirements:**
- Don't rely solely on AI knowledge - use the provided seed data (hotels, flights, experiences)
- Ensure responses are grounded in the retrieved travel data
- Handle cases where no relevant context is found in the catalogues
- Update or add a new README file with the python run time version and a summary of what you would improve to boost code clarity, maintainability, and production readiness if you had more time.

### Example Request

```json
POST /travel-assistant
Content-Type: application/json

{
  "query": "Where should I go for a solo foodie trip to Asia in September?"
}

```

---

## 📤 Supplying Your Code

Please create and commit your code into a **public GitHub repository** and supply the link to the recruiter for review.

Thanks for your time, we look forward to hearing from you!
