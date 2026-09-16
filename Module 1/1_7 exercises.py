import functools
import time


def token_cost(tokens: int, model: str) -> float:
    """Return the estimated cost for a number of tokens."""
    costs_per_1k = {
        "gpt-4o-mini": 0.00015,
        "gpt-4o": 0.005,
        "claude-3-haiku": 0.00025,
    }

    if model not in costs_per_1k:
        raise ValueError(f"Unknown model: {model}")

    return tokens / 1000 * costs_per_1k[model]


def retry(max_retries: int, delay: float = 0.0):
    """Retry a function after exceptions, up to max_retries times."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_retries:
                        raise
                    if delay:
                        time.sleep(delay)

        return wrapper

    return decorator


attempts = 0


@retry(max_retries=2)
def function_that_fails_twice() -> str:
    """Fail twice, then return successfully."""
    global attempts
    attempts += 1
    if attempts <= 2:
        raise RuntimeError("Temporary failure")
    return "Success"


def temperature_label(t: float) -> str:
    """Return a label for a temperature from 0.0 through 1.0."""
    if not 0.0 <= t <= 1.0:
        raise ValueError("temperature must be between 0.0 and 1.0")
    if t <= 0.3:
        return "precise"
    if t <= 0.7:
        return "balanced"
    return "creative"


def parse_usage(text: str) -> tuple[int, float]:
    """Parse token count and price from a usage description."""
    token_part, cost_part = text.split(",")
    tokens = int(token_part.strip().split()[0])
    cost = float(cost_part.strip().split()[0])
    return tokens, cost


print(token_cost(2000, "gpt-4o"))
print(function_that_fails_twice())
print(temperature_label(0.2))
print(temperature_label(0.5))
print(temperature_label(0.9))
print(parse_usage("128000 tokens, 0.005 USD per 1K"))