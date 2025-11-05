.PHONY: test

test:
	uv run python -m src.main zip test.zip test
help:
	uv run python -m src.main cd --help
clean:
	rm -r ./src/logs/*
mypy:
	uv run mypy src
