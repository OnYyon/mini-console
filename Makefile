.PHONY: test

test:
	uv run python -m src.main untar ./Desktop/abs1.tar.gz
help:
	uv run python -m src.main --help
clean:
	rm -r ./src/logs/*
mypy:
	uv run mypy src
