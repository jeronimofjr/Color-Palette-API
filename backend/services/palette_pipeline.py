"""
Serviço responsável pela pipeline de processamento da imagem.
"""

from backend.services.extract_color import extract_colors
from backend.services.palette_generator import append_palette_to_image
from backend.utils.image_utils import image_to_pixels, resize_image, image_to_png_bytes
import numpy as np
from typing import List, Dict


def process_palette(image: np.ndarray, n_colors: int) -> tuple[List[Dict], bytes]:
    """
    Organiza as chamadas do processamento da imagem.
    """

    small_image = resize_image(image)
    pixels = image_to_pixels(small_image)
    color_palette = extract_colors(pixels, n_colors)
    image_combined = append_palette_to_image(image, color_palette, n_colors)
    png_bytes = image_to_png_bytes(image_combined)

    return color_palette, png_bytes
