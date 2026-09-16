def embed_texts(texts: list[str]) -> list[list[float]]:
    """Return deterministic demo embeddings for text values."""
    return [
        [hash(text) % 100 / 100.0, 0.42, 0.87]
        for text in texts
    ]
