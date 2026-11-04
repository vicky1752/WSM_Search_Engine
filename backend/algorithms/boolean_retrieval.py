
from algorithms.preprocessing import preprocess_text


def boolean_search(query, index, documents):

    words = query.lower().split()

    # Extract search terms
    terms = [
        word for word in words
        if word.upper() not in ["AND", "OR", "NOT"]
    ]

    if not terms:
        return []

    # Find document IDs for each term
    postings = []

    for term in terms:
        cleaned = preprocess_text(term)

        if not cleaned:
            postings.append(set())
        else:
            term = cleaned[0]
            doc_ids = set(index.get(term, {}).keys())
            postings.append(doc_ids)

    # Handle AND
    if "AND" in [word.upper() for word in words]:
        result = postings[0]

        for posting in postings[1:]:
            result = result.intersection(posting)

    # Handle OR
    elif "OR" in [word.upper() for word in words]:
        result = set()

        for posting in postings:
            result = result.union(posting)

    # Handle NOT (first term NOT second term)
    elif "NOT" in [word.upper() for word in words]:
        if len(postings) < 2:
            return []

        result = postings[0] - postings[1]

    else:
        result = set().union(*postings)

    # Return matching documents
    return [
        doc for doc in documents
        if doc["id"] in result
    ]

