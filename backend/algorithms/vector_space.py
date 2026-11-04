
import math


def cosine_similarity(vector_a, vector_b):

    # Calculate dot product
    dot_product = sum(
        value * vector_b.get(term, 0)
        for term, value in vector_a.items()
    )

    # Calculate vector magnitudes
    magnitude_a = math.sqrt(
        sum(value ** 2 for value in vector_a.values())
    )

    magnitude_b = math.sqrt(
        sum(value ** 2 for value in vector_b.values())
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (magnitude_a * magnitude_b)
