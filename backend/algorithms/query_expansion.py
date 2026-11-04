
from algorithms.preprocessing import preprocess_text

SYNONYMS = {
    "story": ["stories", "tale", "narrative"],
    "happy": ["joyful", "pleased", "glad"],
    "computer": ["machine", "system", "device"],
    "search": ["retrieval", "finding", "lookup"],
    "author": ["writer", "novelist", "creator"]
}


def expand_query(query):

    terms = preprocess_text(query)
    expanded_terms = list(terms)

    for term in terms:
        related = SYNONYMS.get(term, [])
        expanded_terms.extend(related)

    return list(dict.fromkeys(expanded_terms))

