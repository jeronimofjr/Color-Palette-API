"""
Processa uma imagem para extrair sua paleta de cores e gera uma nova versão da imagem com a paleta anexada.
Retorna a lista de cores em formato RGB/Hex e a imagem final codificada em Base64.
"""

from fastapi import APIRouter, File, UploadFile, Form, status
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
        return JSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            content={
                "code": "UNSUPPORTED_IMAGE_TYPE",
                "detail": "Formato não suportado. Envie apenas imagens PNG ou JPEG.",
            },
        )

    file_bytes = await file.read()

    if not file_bytes:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": "EMPTY_FILE",
                "detail": "Arquivo de imagem vazio.",
            },
        )

    try:
        image = bytes_to_image(file_bytes)
        color_palette, png_bytes = process_palette(image, n_colors)
        encoded_image = base64.b64encode(png_bytes).decode("utf-8")

    except ValueError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": "INVALID_IMAGE",
                "detail": (
                    "Não foi possível ler a imagem. "
                    "O arquivo pode estar corrompido."
                ),
            },
        )

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": "PALETTE_PROCESSING_ERROR",
                "detail": "Ocorreu um erro interno ao processar a imagem.",
            },
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "colors": color_palette,
            "image_base64": f"data:image/png;base64,{encoded_image}",
        },
    )
