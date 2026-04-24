init:
	uv sync

test:
	# This runs all of the tests. To run an individual test, run pytest with
	# the -k flag, like "uv run pytest -k test_path_is_not_double_encoded"
	uv run pytest tests
	uv run ruff check .
