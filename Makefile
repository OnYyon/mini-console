.PHONY: test

test:
	uv run python -m src.main cd
help:
	uv run python -m src.main cd --help
clean:
	rm -r ./src/logs/*

test_mgr:
	 uv run python -m src.utils.dot_manager

mypy:
	uv run mypy src
