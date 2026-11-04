
def calculate_metrics(relevant_documents, retrieved_documents):

    relevant = set(relevant_documents)
    retrieved = set(retrieved_documents)

    true_positive = len(relevant & retrieved)

    precision = (
        true_positive / len(retrieved)
        if retrieved else 0
    )

    recall = (
        true_positive / len(relevant)
        if relevant else 0
    )

    f1_score = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0
    )

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1_score, 4)
    }

