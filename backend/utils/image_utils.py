import numpy as np
import cv2

def resize_image(image: np.ndarray, max_dimension: int = 400) -> np.ndarray:
    """
    Redimensiona a imagem mantendo a proporção, de forma que a maior
    dimensão não exceda `max_dimension`. Isso reduz drasticamente o
    custo computacional do K-Means sem comprometer a distribuição
    geral das cores.
    """
    height, width = image.shape[:2]
    largest_side = max(height, width)

    if largest_side <= max_dimension:
        return image

    scale = max_dimension / largest_side
    new_width = int(width * scale)
    new_height = int(height * scale)

    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized

def image_to_pixels(image: np.ndarray) -> np.ndarray:
    """
    Transforma uma imagem (altura x largura x 3) em uma lista de
    pixels no formato (n_pixels, 3), convertendo de BGR para RGB.
    """

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = image_rgb.reshape((-1, 3))
    pixels = np.float32(pixels)
    return pixels

def rgb_to_hex(rgb: np.ndarray) -> str:
    """
    Converte um array [R, G, B] (0-255) para uma string hexadecimal,
    ex: [30, 144, 255] -> "#1E90FF"
    """
    
    r, g, b = rgb
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    return f"#{r:02X}{g:02X}{b:02X}"