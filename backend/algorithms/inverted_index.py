
from collections import defaultdict
from algorithms.preprocessing import preprocess_text


def build_inverted_index(documents):

    # Each term will store its document IDs and positions
    index = defaultdict(lambda: defaultdict(list))

    for doc in documents:

        doc_id = doc["id"]
        text = doc["text"]

        # Preprocess document text
        words = preprocess_text(text)

        # Store word positions
        for position, word in enumerate(words):

            index[word][doc_id].append(position)

    return index
