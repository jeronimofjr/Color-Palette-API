"""
Serviço responsável por extrair as cores da imagem a partir do algoritmo K-Means.
"""

import numpy as np
from typing import List, Dict
from sklearn.cluster import KMeans

from backend.utils.image_utils import rgb_to_hex

def extract_colors(
    pixels: np.ndarray,
    n_colors: int = 10,
    random_state: int = 42,
) -> List[Dict]:
    """
    Aplica K-Means sobre os pixels de uma imagem
    para identificar as cores dominantes.

    Retorna uma lista de dicionários com as cores no formato rgb e hexadecimal, no formato:

    {
        "rgb": [r, g, b],
        "hex": "#RRGGBB",
    }
    """
    n_clusters = min(n_colors, len(pixels))

   
    model = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10,
    )

    labels = model.fit_predict(pixels)
    centers = model.cluster_centers_

    total_pixels = len(labels)
    labels = np.unique(labels)

    colors = []
    for label in labels:
        rgb = np.int16(centers[label]).tolist()
        

        colors.append({
            "rgb": rgb,
            "hex": rgb_to_hex(rgb),
        })

    return colors