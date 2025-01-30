import logging


def setup_logging(is_debug: bool = False):
    logging.basicConfig(
        level=(logging.DEBUG if is_debug else logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log"),
        ],
    )
