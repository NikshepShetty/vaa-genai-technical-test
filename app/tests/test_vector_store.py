"""
Chroma vector store test file
Run from repo root: pytest
"""

from app.vector_store import VectorStoreService

def test_vector_store_initialisation():
    """ Test to check vector store initialises without error."""
    vs = VectorStoreService()
    assert vs.collection is not None

def test_load_help_content_works():
    """ Test to check help content loads into the vector store."""
    vs = VectorStoreService()
    vs.load_help_content()

    count = vs.collection.count()
    assert count > 0

def test_get_category_list_sorted_and_lowercase():
    """ Test to check category list is sorted and lowercase."""
    vs = VectorStoreService()
    vs.load_help_content()

    categories = vs.get_category_list()
    assert isinstance(categories, list)
    assert categories == sorted(categories)
    assert all(cat == cat.lower() for cat in categories)

def test_search_returns_list():
    """ Test to check search returns a list."""
    vs = VectorStoreService()
    vs.load_help_content()

    results = vs.search("What is the customer support number?")
    assert isinstance(results, list)

def test_search_result_shape():
    """ Test to check search result contains expected keys and types."""
    vs = VectorStoreService()
    vs.load_help_content()

    results = vs.search("What is the customer support number?", top_k=1)

    if len(results) > 0:
        result = results[0]
        assert "text" in result
        assert "source_id" in result
        assert "score" in result

        assert isinstance(result["text"], str)
        assert isinstance(result["source_id"], str)
        assert result["score"] is None or isinstance(result["score"], float)

def test_search_score_valid_cosine_range():
    """ Test to check score is within a valid cosine similarity range."""
    vs = VectorStoreService()
    vs.load_help_content()

    results = vs.search("What is the customer support number?", top_k=3)
    for r in results:
        if r["score"] is not None:
            assert 0.0 <= r["score"] <= 1.0

def test_search_with_category_filter():
    """ Test to check search works with valid category filter."""
    vs = VectorStoreService()
    vs.load_help_content()

    categories = vs.get_category_list()
    assert len(categories) > 0

    response = vs.search(query="What is the customer support number?", category=categories[0], top_k=3)
    assert isinstance(response, list)

def test_search_with_negative_top_k():
    """ Test to check search with negative top_k does not raise error and returns a list."""
    vs = VectorStoreService()
    vs.load_help_content()

    results = vs.search("What is the customer support number?", top_k=-5)
    assert isinstance(results, list)

def test_search_with_very_large_top_k():
    """ Test to check search with very large top_k does not raise error and returns a list."""
    vs = VectorStoreService()
    vs.load_help_content()

    results = vs.search("What is the customer support number?", top_k=1000000)
    assert isinstance(results, list)