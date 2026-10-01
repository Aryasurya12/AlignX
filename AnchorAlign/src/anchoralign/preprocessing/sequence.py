def preprocess_sequence(seq: str) -> str:
    if not seq:
        return seq
    seq = seq.upper()
    valid_chars = set("ACGTN")
    if not all(c in valid_chars for c in seq):
        raise ValueError("Invalid DNA sequence characters found.")
    return seq
