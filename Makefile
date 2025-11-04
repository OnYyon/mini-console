.PHONY: test

test:
	uv run python -m src.main ls -al
help:
	uv run python -m src.main cd --help
clean:
	rm -r ./src/logs/*
