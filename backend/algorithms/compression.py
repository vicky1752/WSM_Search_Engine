
def gap_encode(postings):
    """Compress sorted document IDs using gap encoding."""

    if not postings:
        return []

    gaps = [postings[0]]

    for i in range(1, len(postings)):
        gaps.append(postings[i] - postings[i - 1])

    return gaps


def gap_decode(gaps):
    """Reconstruct document IDs from gaps."""

    if not gaps:
        return []

    postings = [gaps[0]]

    for gap in gaps[1:]:
        postings.append(postings[-1] + gap)

    return postings


def variable_byte_encode(number):

    if number < 0:
        raise ValueError("Number must be non-negative")

    if number == 0:
        return [128]

    result = []

    while number > 0:
        result.insert(0, number % 128)
        number //= 128

    result[-1] += 128

    return result
