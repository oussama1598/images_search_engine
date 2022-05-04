import fastapi
from starlette.responses import RedirectResponse

from backend.src.api.endpoints import mnist

router = fastapi.APIRouter(
    prefix='/api/v1'
)


@router.get('/')
async def api_index():
    return RedirectResponse('/docs')


router.include_router(mnist.router)
