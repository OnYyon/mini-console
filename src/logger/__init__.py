import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] | %(name)-15s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("./src/logs/shell.log", encoding='utf-8')
    ]
)
