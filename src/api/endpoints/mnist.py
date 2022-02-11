import base64

import cv2
import fastapi
import magic
import numpy as np
from fastapi import UploadFile
from starlette.responses import JSONResponse

from src.services import mnist_service

router = fastapi.APIRouter(
    prefix='/mnist'
)


@router.post('/predict')
async def mnist_predict(file: UploadFile, neighbors: int = 10):
    file_bytes: bytes = file.file.read()

    mime_type: str = magic.from_buffer(file_bytes, mime=True)

    if 'image' not in mime_type:
        return JSONResponse(
            content={
                'status': False,
                'error': 'File must be an image.'
            },
            status_code=400
        )

    jpg_as_np = np.frombuffer(file_bytes, dtype=np.uint8)
    uploaded_image = cv2.imdecode(jpg_as_np, cv2.IMREAD_GRAYSCALE)
    encoded_image = mnist_service.encode_image(uploaded_image)[0]

    neighbors_images = mnist_service.get_image_neighbors(encoded_image, neighbors)

    return [
        base64.b64encode(cv2.imencode('.png', image)[1])
        for image in neighbors_images
    ]
