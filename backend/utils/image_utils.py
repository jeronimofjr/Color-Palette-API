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
