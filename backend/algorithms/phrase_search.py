
from algorithms.preprocessing import preprocess_text


def phrase_search(query, index, documents):

    terms = preprocess_text(query)

    if not terms:
        return []

    # Get document IDs containing the first word
    candidate_docs = set(index.get(terms[0], {}).keys())

    # Keep documents containing every phrase word
    for term in terms[1:]:
        candidate_docs &= set(index.get(term, {}).keys())

    results = []

    for doc_id in candidate_docs:

        # Get positions of the first word
        first_positions = index[terms[0]][doc_id]

        # Check consecutive positions
        for position in first_positions:

            match = True

            for offset, term in enumerate(terms[1:], start=1):

                positions = index[term][doc_id]

                if position + offset not in positions:
                    match = False
                    break

            if match:
                results.append(doc_id)
                break

    return [
        doc for doc in documents
        if doc["id"] in results
    ]

