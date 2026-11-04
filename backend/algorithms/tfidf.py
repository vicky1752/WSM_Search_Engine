
import math
from collections import Counter
from algorithms.preprocessing import preprocess_text


def calculate_tfidf(documents):

    total_documents = len(documents)

    if total_documents == 0:
        return {}

    document_terms = {}
    document_frequency = Counter()

    # Process every document
    for doc in documents:

        words = preprocess_text(doc["text"])
        document_terms[doc["id"]] = Counter(words)

        # Count each term once per document
        for term in set(words):
            document_frequency[term] += 1

    tfidf_scores = {}

    # Calculate TF-IDF
    for doc_id, term_counts in document_terms.items():

        total_terms = sum(term_counts.values())
        tfidf_scores[doc_id] = {}

        for term, count in term_counts.items():

            tf = count / total_terms

            idf = math.log(
                (total_documents + 1) /
                (document_frequency[term] + 1)
            ) + 1

            tfidf_scores[doc_id][term] = tf * idf

    return tfidf_scores
