.PHONY: test

UV = /home/onyyon/.local/bin/uv

test:
	$(UV) run python -m src.main ls
help:
	$(UV) run python -m src.main --help
clean:
	rm -r ./src/logs/*
mypy:
	$(UV) run mypy src
