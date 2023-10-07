from starlette.staticfiles import StaticFiles

from .api import app

app.mount("/prettymaps", StaticFiles(directory="prettymaps"), name="static")
