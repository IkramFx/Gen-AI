import functools
import time
from collections import deque
from string import Formatter
from typing import Callable, TypeVar

from module3 import ConversationHistory, LLMConfig


class RateLimiter:
    """Allow at most max_calls during each time window."""

    def __init__(self, max_calls: int, window_seconds: float = 60.0):
        if max_calls < 1:
            raise ValueError("max_calls must be at least 1")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than 0")
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._calls = deque()

    def check_and_wait(self) -> None:
        """Wait until another call is allowed."""
        while True:
            now = time.monotonic()
            while self._calls and now - self._calls[0] >= self.window_seconds:
                self._calls.popleft()

            if len(self._calls) < self.max_calls:
                self._calls.append(now)
                return

            wait_time = self.window_seconds - (now - self._calls[0])
            time.sleep(max(wait_time, 0))


class PromptTemplate:
    """Template that validates placeholders before rendering."""

    def __init__(self, template: str):
        self.template = template
        self._placeholders = {
            field_name.split(".", 1)[0].split("[", 1)[0]
            for _, field_name, _, _ in Formatter().parse(template)
            if field_name is not None
        }

    def render(self, **kwargs) -> str:
        missing = self._placeholders - kwargs.keys()
        if missing:
            names = ", ".join(sorted(missing))
            raise ValueError(f"Missing template values: {names}")
        return self.template.format_map(kwargs)


T = TypeVar("T", bound=Callable)


def retry(max_attempts: int = 3, delay: float = 0.1):
    """Retry a function until it succeeds or max_attempts is reached."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    if delay < 0:
        raise ValueError("delay cannot be negative")

    def decorator(func: T) -> T:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator


attempts = 0


@retry(max_attempts=3, delay=0.1)
def flaky_function() -> str:
    global attempts
    attempts += 1
    if attempts <= 2:
        raise RuntimeError("Temporary failure")
    return "Success after two failures"


# Exercise 1: use a short window so the demonstration does not wait a minute.
limiter = RateLimiter(max_calls=2, window_seconds=0.01)
for call_number in range(5):
    limiter.check_and_wait()
    print(f"Rate-limited call {call_number + 1}")

# Exercise 2
prompt = PromptTemplate("Explain {topic} for a {audience}.")
print(prompt.render(topic="generator", audience="beginner"))

# Exercise 3
print(flaky_function())

# Exercise 4: package exports
history = ConversationHistory(max_turns=2)
history.add("user", "What is an embedding?")
config = LLMConfig(model="claude-sonnet-4-5", temperature=0.3)
print(history)
print(config.as_dict)