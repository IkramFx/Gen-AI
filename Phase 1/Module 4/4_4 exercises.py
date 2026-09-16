import asyncio
import csv
import json
import os
import threading
import time
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx


# 1. Save and load conversation history as JSON.
def save_conversation(history: list[dict], path: str) -> None:
	"""Serialize conversation history to a JSON file."""
	output_path = Path(path)
	output_path.write_text(
		json.dumps(history, indent=2, ensure_ascii=False),
		encoding="utf-8",
	)


def load_conversation(path: str) -> list[dict]:
	"""Deserialize conversation history from a JSON file."""
	input_path = Path(path)
	data = json.loads(input_path.read_text(encoding="utf-8"))
	if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
		raise ValueError("Conversation history must be a list of dictionaries")
	return data


# 2. Fetch endpoints concurrently and measure their response times.
async def compare_endpoints(urls: list[str]) -> list[tuple[str, int, float]]:
	"""Return URL, status code, and response time in milliseconds for each URL."""
	async def fetch(url: str) -> tuple[str, int, float]:
		start = time.perf_counter()
		try:
			async with httpx.AsyncClient() as client:
				response = await client.get(url, timeout=10.0)
			status_code = response.status_code
		except httpx.HTTPError:
			status_code = 0
		response_time_ms = (time.perf_counter() - start) * 1000
		return url, status_code, response_time_ms

	return list(await asyncio.gather(*(fetch(url) for url in urls)))


# 3. Load JSON config and apply environment overrides.
def _environment_value(value: str, original: Any) -> Any:
	"""Convert an environment string to the type used by the JSON value."""
	if isinstance(original, bool):
		return value.lower() in {"1", "true", "yes", "on"}
	if isinstance(original, int) and not isinstance(original, bool):
		return int(value)
	if isinstance(original, float):
		return float(value)
	if isinstance(original, (dict, list)):
		return json.loads(value)
	return value


def load_config(path: str) -> dict[str, Any]:
	"""Load JSON config and override values with uppercase environment names."""
	config = json.loads(Path(path).read_text(encoding="utf-8"))
	if not isinstance(config, dict):
		raise ValueError("Config file must contain a JSON object")

	merged = deepcopy(config)

	def apply_overrides(section: dict[str, Any], prefix: str = "") -> None:
		for key, original in section.items():
			env_name = f"{prefix}_{key}".upper() if prefix else key.upper()
			if isinstance(original, dict):
				apply_overrides(original, env_name)
			elif env_name in os.environ:
				section[key] = _environment_value(os.environ[env_name], original)

	apply_overrides(merged)
	return merged


# 4. Thread-safe CSV logger for LLM calls.
class LLMCallLogger:
	"""Append one thread-safe CSV row for each LLM call."""

	fieldnames = [
		"timestamp",
		"model",
		"input_tokens",
		"output_tokens",
		"latency_ms",
	]

	def __init__(self, path: str):
		self.path = Path(path)
		self._lock = threading.Lock()
		if not self.path.exists() or self.path.stat().st_size == 0:
			with self.path.open("w", newline="", encoding="utf-8") as file:
				csv.DictWriter(file, fieldnames=self.fieldnames).writeheader()

	def log(
		self,
		model: str,
		input_tokens: int,
		output_tokens: int,
		latency_ms: float,
	) -> None:
		"""Append one LLM call record to the CSV file."""
		row = {
			"timestamp": datetime.now(timezone.utc).isoformat(),
			"model": model,
			"input_tokens": input_tokens,
			"output_tokens": output_tokens,
			"latency_ms": latency_ms,
		}
		with self._lock:
			with self.path.open("a", newline="", encoding="utf-8") as file:
				csv.DictWriter(file, fieldnames=self.fieldnames).writerow(row)


if __name__ == "__main__":
	conversation_path = "conversation.json"
	conversation = [
		{"role": "user", "content": "What is RAG?"},
		{"role": "assistant", "content": "RAG retrieves context before generation."},
	]
	save_conversation(conversation, conversation_path)
	print(load_conversation(conversation_path))

	config_path = "config.json"
	Path(config_path).write_text(
		json.dumps({"model": "gpt-4o", "temperature": 0.7}),
		encoding="utf-8",
	)
	os.environ["TEMPERATURE"] = "0.2"
	print(load_config(config_path))

	logger = LLMCallLogger("llm_calls.csv")
	logger.log("gpt-4o", 100, 42, 315.5)
	print("CSV call logged")

	endpoint_results = asyncio.run(
		compare_endpoints(["https://jsonplaceholder.typicode.com/posts/1"])
	)
	print(endpoint_results)
