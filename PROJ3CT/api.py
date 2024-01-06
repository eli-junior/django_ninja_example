from ninja import NinjaAPI

from .cadastro.api import router as cadastro_router


api = NinjaAPI()

api.add_router("/cadastro", cadastro_router)
