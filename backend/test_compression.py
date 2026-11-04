from algorithms.compression import (
    gap_encode,
    gap_decode,
    variable_byte_encode
)

postings = [2, 5, 9, 15]

gaps = gap_encode(postings)

print("Original:", postings)
print("Gap encoded:", gaps)
print("Decoded:", gap_decode(gaps))
print("Variable byte:", variable_byte_encode(130))