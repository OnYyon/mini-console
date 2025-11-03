.PHONY: test

test:
	uv run python -m src.main ls -al ~root
help:
	uv run python -m src.main cd --help
clean:
	rm -r ./src/logs/*
