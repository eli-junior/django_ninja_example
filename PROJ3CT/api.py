from ninja import NinjaAPI

from .cadastro.api import router as cadastro_router
from .futebol.api import router as futebol_router


api = NinjaAPI()

api.add_router("/cadastro", cadastro_router)
api.add_router("futebol/", futebol_router)
