from ninja import NinjaAPI

from .futebol.api import router as futebol_router


api = NinjaAPI(version="1.0.0")

api.add_router("futebol/", futebol_router)
