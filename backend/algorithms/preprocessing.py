
import re

# Common English words that we don't need for basic searching
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "in", "on", "at", "to", "of", "for", "and",
    "or", "but", "with", "this", "that", "it",
    "as", "by", "from", "be", "been", "has", "have"
}


def preprocess_text(text):
    # Convert all text to lowercase
    text = text.lower()

    # Extract words and remove punctuation
    words = re.findall(r"\b[a-z0-9]+\b", text)

    # Remove stop words
    words = [word for word in words if word not in STOP_WORDS]

    return words
