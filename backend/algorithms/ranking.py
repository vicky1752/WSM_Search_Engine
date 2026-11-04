
from collections import Counter
from algorithms.preprocessing import preprocess_text
from algorithms.tfidf import calculate_tfidf
from algorithms.vector_space import cosine_similarity


def rank_documents(query, documents):

    if not documents:
        return []

    # Calculate document vectors
    document_vectors = calculate_tfidf(documents)

    # Process query
    query_terms = preprocess_text(query)
    query_counts = Counter(query_terms)

    total_query_terms = sum(query_counts.values())

    if total_query_terms == 0:
        return []

    # Calculate query term frequencies
    query_vector = {}

    for term, count in query_counts.items():
        query_vector[term] = count / total_query_terms

    # Rank documents
    ranked_results = []

    for doc in documents:

        doc_vector = document_vectors.get(doc["id"], {})

        score = cosine_similarity(
            query_vector,
            doc_vector
        )

        if score > 0:
            ranked_results.append({
                "id": doc["id"],
                "name": doc["name"],
                "text": doc["text"],
                "score": score
            })

    ranked_results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return ranked_results

