from hashlib import sha256
from pathlib import Path

import numpy as np
import pandas as pd


# 1. Load benchmark scores and calculate model/task statistics.
BENCHMARK_PATH = Path(__file__).with_name("benchmark_scores.csv")
benchmark = pd.read_csv(BENCHMARK_PATH)

mean_score_per_model = benchmark.groupby("model")["score"].mean().sort_values(
    ascending=False
)
best_task_per_model = benchmark.loc[
    benchmark.groupby("model")["score"].idxmax(), ["model", "task", "score"]
].sort_values("model")
score_latency_correlation = benchmark["score"].corr(benchmark["latency_ms"])

print("Mean score per model:")
print(mean_score_per_model)
print("\nBest-performing task per model:")
print(best_task_per_model.to_string(index=False))
print(f"\nScore/latency correlation: {score_latency_correlation:.4f}")


# 2. L2-normalise every row in an embedding matrix.
def normalise_embeddings(matrix: np.ndarray) -> np.ndarray:
    """Return a copy with each row normalised to unit L2 length."""
    matrix = np.asarray(matrix, dtype=float)
    row_norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    safe_norms = np.where(row_norms == 0, 1.0, row_norms)
    return matrix / safe_norms


embeddings = np.array([[3.0, 4.0], [1.0, 2.0], [5.0, 12.0]])
normalised = normalise_embeddings(embeddings)
print("\nNormalised row norms:", np.linalg.norm(normalised, axis=1))


# 3. Read .txt files and return counts sorted by word count.
def inspect_text_folder(folder: str) -> pd.DataFrame:
    """Return filename and text statistics for every .txt file in a folder."""
    records = []
    for path in sorted(Path(folder).glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        records.append(
            {
                "filename": path.name,
                "char_count": len(text),
                "word_count": len(text.split()),
                "sentence_count": sum(text.count(mark) for mark in ".!?")
                or (1 if text.strip() else 0),
            }
        )
    return pd.DataFrame(
        records,
        columns=["filename", "char_count", "word_count", "sentence_count"],
    ).sort_values("word_count", ascending=False, ignore_index=True)


text_stats = inspect_text_folder(Path(__file__).with_name("text_samples"))
print("\nText statistics:")
print(text_stats.to_string(index=False))


# 4. Build pairwise cosine similarities using deterministic hash embeddings.
def hash_embedding(text: str, dimensions: int = 32) -> np.ndarray:
    """Create a deterministic mock embedding from a text hash."""
    digest = sha256(text.encode("utf-8")).digest()
    values = (digest * ((dimensions // len(digest)) + 1))[:dimensions]
    vector = np.array([value / 255.0 for value in values])
    return vector / np.linalg.norm(vector)


corpus = [
    "RAG retrieves context for generation.",
    "Retrieval augmented generation uses relevant documents.",
    "Python is useful for data analysis.",
    "Embeddings represent text as numerical vectors.",
    "A language model generates a response from a prompt.",
]
corpus_embeddings = np.vstack([hash_embedding(text) for text in corpus])
similarity_matrix = corpus_embeddings @ corpus_embeddings.T
np.fill_diagonal(similarity_matrix, -np.inf)
best_pair = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)

print("\nHighest-similarity pair:")
print(f"Pair: ({best_pair[0]}, {best_pair[1]})")
print(f"Similarity: {similarity_matrix[best_pair]:.4f}")
print(f"Text 1: {corpus[best_pair[0]]}")
print(f"Text 2: {corpus[best_pair[1]]}")
