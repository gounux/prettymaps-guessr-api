import logging
import sys

import colorlog
from starlette.staticfiles import StaticFiles

from api.api import app

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = colorlog.ColoredFormatter(
    "%(yellow)s%(asctime)s %(log_color)s[%(levelname)s]%(reset)s %(purple)s[%(name)s %(module)s]%(reset)s %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


app.mount("/prettymaps", StaticFiles(directory="prettymaps"), name="static")
