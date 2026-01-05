## Installation Instructions

- Requires at least Python 3.11
- Create a `.env` file in the project root and add your OpenAI key:
  ```
  OPENAI_API_KEY=your_key_here
  ```
- Install dependencies:
  ```
  pip install -r requirements.txt
  ```
- Run the API:
  ```
  python -m uvicorn app.main:app --reload
  ```
I used UV to create the virtual environment for this process.

I wanted to create this notes section to document the reasoning behind my choice. Even though those are explained in the comments for the code, I could go into much more detail here and make it easier to show you the bigger picture.

The first step was to look at the dataset itself (present in help_content.json). It is a help manual for virgin atlantic customers with 4 keys - ids, title, category and content. The content is very long, roughly 350 characters max, which easily fits within the LLM's context windows. There are 12 entries. This led me to decide that no complex chunking strategy is required for this case. 1 json entry should be treated as one chunk. If the content field was longer (regularly 500+ characters), we could have used a mix of recursive and sliding window chunking.

## Vector Store

I decided to start with vector_store.py file for implementation first. For the vector DB, I had a couple choices- a dedicated vector DB like chromaDB or Faiss, or use something PGvector that could be used along with postgresql, meaning regular databases and vectorDBs can sit together making management easier. As this project is on a very small scale and I already had experience with Chroma, I decided to move forward with that.

After that, I moved on to the retrieval part. Since each json entry is treated as a single chunk, retrieval is fairly simple, especially with Chroma. I used the small embedding model from OpenAI as the embedding function for the chroma collection. For the confidence score, chroma retrieves chunk by comparing the vector embedding distance between the query and the chunk. By default this is done using squared L2 (euclidian) distance, but I changed it the cosine distance which gives us a better measure due to it picking up directional information well ( https://razikus.substack.com/p/chromadb-defaults-to-l2-distance-why-that-might-not-be-the-best-choice-ac3d47461245 ). The chroma function uses cosine distance (1 - cosine similarity), so it had to be converted and grounded (cosine has a range from -1 to 1, grounded all negative values to 0) later on. Each chunk is stored with metadata such as id, title, and category. The category field is useful for optional filtering, so if the user provides a category, the search can be narrowed down to only relevant sections, this was done using chroma's where argument inside the query function. I altered schema.py to include an optional category in TravelQuery as well. validations were added to make sure only categories that actually exist in the dataset are accepted, rather than silently failing or returning empty results.

I wanted to test the system with and without a reranker to check if the reranker added much value to the RAG system, the ms-marco-MiniLM-L-6-v2 was used as the reranker model and I set a flag in the class constructor called _reranker which could be used to use/not use this reranker. Currently, its set to false as it didnt have any difference on the final results and would have just made the overall system slower. Maybe it would make more sense for a larger system.

I mostly left the prompt unchanged as the answers were accurate and to the point, but added some safeguards for explicit language or prompt injection attempts.

## Main

Next, I moved to the main.py file, where the main focus on controlling the flow and making sure different exceptions were handled properly. Apart from that, how would the confidence scores going to be displayed, I had cosine similarity for each chunk to the query, so I first tried to do a reciprocal weight average where the first ranked chunk had full weight, second had 50% and so on. But this didn't work as well for the dataset as in most cases the questions could be answered only using the first ranked chunk, so even if the answer seemed confident and accurate with its answers, the second ranked chunk onwards would drag the score down. So, I decided to have the first ranked chunk cosine similarity as the confidence score. The score is always coming from chroma, even if a reranker is used. This is because the reranker doesn't really have a fixed range unlike cosine's [-1,1], so converting them to a percentage would be consistent. I have also added type hint to the functions (both for variables and function argument/returns) to make it easier to understand what comes in and goes out of each function and variable.

## Evaluation

For evaluation, I didn’t want to rely only on manually checking a few responses (even though the responses looks accurate to the naked eye), so I used RAGAS library to get some numerical indicators on how the system was performing. I set up a small evaluation set with a mix of valid help questions, travel questions which can't be answered from the dataset, complete nonsense queries and a few prompt injection or unsafe requests. This made it easier to see how the system behaves across different scenarios and check for any vulnerabilities. I measured metrics like faithfulness, answer relevancy, answer correctness, and context precision/recall. Faithfulness was useful to check whether the model was sticking to the retrieved context. Answer relevancy and correctness helped confirm that the responses actually addressed the user’s question when an answer existed. Context precision and recall helped validate whether the retrieval step was pulling the right chunks and not adding too much noise. I ran these evaluations with and without the reranker enabled to compare the impact. 

| Metric             | Without Reranker | With Reranker |
|--------------------|------------------|---------------|
| Faithfulness       | 0.68             | 0.60          |
| Answer Relevancy   | 0.57             | 0.56          |
| Answer Correctness | 0.85             | 0.87          |
| Context Precision  | 0.76             | 0.74          |
| Context Recall     | 0.82             | 0.82          |

While there are slight improvements with reranker here, these are not big enough to warrant using a reranker with the current dataset. Also, the responses themselves have a bit of randomness which could explain the small difference in scores.

## Testing

For testing, I focused on making sure the system behaves correctly at the boundaries rather than testing external libraries, like chroma, themselves. API tests were added to check request validation, required fields, optional parameters like category and top_k, and response structure. This includes testing invalid inputs such as empty queries, incorrect data types, and extreme values for top_k to ensure proper exception handling that I implemented in the main file.

Vector store tests focus on ingestion and retrieval logic. These tests check that help content is loaded correctly, categories are extracted and validated properly and search results follow the expected format. I also added tests around optional category filtering and edge cases where filters or parameters might not match any content. 

Hopefully, this file and my comments inside the code gave you a better understanding of why I made certain choices to the architecture and implementation.