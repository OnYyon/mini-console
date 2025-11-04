.PHONY: test

test:
	uv run python -m src.main cp -r src/history src/commands
help:
	uv run python -m src.main cd --help
clean:
	rm -r ./src/logs/*
mypy:
	uv run mypy src
