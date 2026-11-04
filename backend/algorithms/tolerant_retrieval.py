
from difflib import get_close_matches
import re


def wildcard_search(query, index, documents):

    pattern = "^" + re.escape(query.lower()).replace(
        r"\*", ".*"
    ) + "$"

    matching_terms = [
        term for term in index
        if re.fullmatch(pattern, term)
    ]

    matching_ids = set()

    for term in matching_terms:
        matching_ids.update(index[term].keys())

    return [
        doc for doc in documents
        if doc["id"] in matching_ids
    ]


def spelling_correction(query, index):

    query = query.lower().strip()

    suggestions = get_close_matches(
        query,
        list(index.keys()),
        n=3,
        cutoff=0.6
    )

    return suggestions

