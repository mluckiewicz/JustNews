import logging

logging.basicConfig(
        format="%(asctime)s | %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.FileHandler("app.log", mode="a", encoding="utf-8")],
        level=logging.DEBUG,
    )

def get_logger(name: str):
    return logging.getLogger(name)
