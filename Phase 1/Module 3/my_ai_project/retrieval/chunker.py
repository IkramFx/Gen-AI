from collections.abc import Generator


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> Generator[str, None, None]:
    """Yield overlapping text chunks."""
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size - 1")

    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        yield text[start:end]
        start += chunk_size - overlap
