"""
Serviço responsável por gerar a representação visual da paleta de
cores e anexá-la à imagem original.
"""

from typing import List, Dict
import cv2
import numpy as np


def append_palette_to_image(
    image: np.ndarray,
    color_palette: List[Dict],
    n_color: int,
) -> np.ndarray:
    """
    Anexa a paleta de cores na parte inferior da imagem original,
    redimensionando a paleta para que sua largura corresponda à da
    imagem, caso necessário.
    """
    image_height, image_width = image.shape[:2]

    colors = []
    for  palette in color_palette:
        colors.append(np.full((image_height // 10, image_width // n_color, 3), palette["rgb"][::-1]))

    palette = np.concatenate(colors, axis=1)
    palette_height, palette_width = palette.shape[:2]

    if palette_width != image_width:
        palette = cv2.resize(
            palette,
            (image_width, palette_height),
            interpolation=cv2.INTER_NEAREST,
        )

    combined = np.vstack((image, palette))

    return combined