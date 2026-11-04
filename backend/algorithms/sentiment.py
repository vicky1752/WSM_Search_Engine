
POSITIVE_WORDS = {
    "good", "great", "excellent", "happy",
    "beautiful", "wonderful", "success", "love",
    "best", "amazing", "positive"
}

NEGATIVE_WORDS = {
    "bad", "poor", "terrible", "sad",
    "hate", "worst", "failure", "negative",
    "awful", "problem", "disappointing"
}


def analyze_sentiment(text):

    words = text.lower().split()

    positive = sum(
        1 for word in words
        if word.strip(".,!?;:") in POSITIVE_WORDS
    )

    negative = sum(
        1 for word in words
        if word.strip(".,!?;:") in NEGATIVE_WORDS
    )

    if positive > negative:
        sentiment = "Positive"

    elif negative > positive:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return {
        "positive": positive,
        "negative": negative,
        "sentiment": sentiment
    }

