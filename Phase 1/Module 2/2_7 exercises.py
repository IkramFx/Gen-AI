from itertools import islice
from typing import Any, Generator, Iterable


# 1. Filter responses under 500 ms and sort them by token count.
api_responses = [
    {"tokens": 1200, "latency_ms": 420},
    {"tokens": 500, "latency_ms": 620},
    {"tokens": 800, "latency_ms": 250},
]

fast_responses = sorted(
    [response for response in api_responses if response["latency_ms"] < 500],
    key=lambda response: response["tokens"],
)


def conversation_stats(messages: list[dict]) -> dict:
    """Return basic statistics for a list of conversation messages."""
    total_messages = len(messages)
    user_turns = sum(message.get("role") == "user" for message in messages)
    assistant_turns = sum(
        message.get("role") == "assistant" for message in messages
    )
    total_words = sum(
        len(str(message.get("content", "")).split()) for message in messages
    )

    return {
        "total_messages": total_messages,
        "user_turns": user_turns,
        "assistant_turns": assistant_turns,
        "avg_words_per_message": (
            total_words / total_messages if total_messages else 0.0
        ),
    }


def batch_items(items: Iterable[Any], batch_size: int) -> Generator[list[Any], None, None]:
    """Yield items in lists containing at most batch_size elements."""
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")

    iterator = iter(items)
    while batch := list(islice(iterator, batch_size)):
        yield batch


# 4. Find models that are both fast and cheap.
fast_models = ["gpt-4o-mini", "claude-3-haiku", "gpt-4o"]
cheap_models = ["claude-3-haiku", "gpt-4o-mini", "llama-3"]
both_fast_and_cheap = set(fast_models) & set(cheap_models)


messages = [
    {"role": "user", "content": "What is a generator?"},
    {"role": "assistant", "content": "A generator produces values lazily."},
    {"role": "user", "content": "Show me an example."},
]

print(fast_responses)
print(conversation_stats(messages))
print(list(batch_items(range(7), 3)))
print(both_fast_and_cheap)