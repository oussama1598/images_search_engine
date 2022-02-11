import fastapi
from starlette.responses import RedirectResponse

router = fastapi.APIRouter(
    prefix='/api/v1'
)


@router.get('/')
async def api_index():
    return RedirectResponse('/docs')
