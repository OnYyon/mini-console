.PHONY: test

test:
	uv run python -m src.main undo
help:
	uv run python -m src.main --help
clean:
	rm -r ./src/logs/*
mypy:
	uv run mypy src
