"""
Processa uma imagem para extrair sua paleta de cores e gera uma nova versão da imagem com a paleta anexada.
Retorna a lista de cores em formato RGB/Hex e a imagem final codificada em Base64.
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse

from backend.utils.image_utils import bytes_to_image

from backend.services.palette_pipeline import process_palette
import base64

router = APIRouter()

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/jpg", "image/png"}


@router.post("/palette")
async def extract_palette(
    file: UploadFile = File(..., description="Imagem JPEG ou PNG"),
    n_colors: int = Form(5, ge=1, le=10, description="Número de cores para extrair"),
):

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Formato de arquivo não suportado: '{file.content_type}'. "
                "Envie uma imagem JPEG ou PNG."
            ),
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(status_code=400, detail="Arquivo de imagem vazio")

    try:

        image = bytes_to_image(file_bytes)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

    color_palette, png_bytes = process_palette(image, n_colors)
    encoded_image = base64.b64encode(png_bytes).decode("utf-8")

    return JSONResponse(
        content={
            "colors": color_palette,
            "image_base64": f"data:image/png;base64,{encoded_image}",
        }
    )
