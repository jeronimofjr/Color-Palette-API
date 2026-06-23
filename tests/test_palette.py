import pytest
import numpy as np
from unittest.mock import patch

from backend.services.extract_color import extract_colors
from backend.services.palette_generator import append_palette_to_image
from backend.services.palette_pipeline import process_palette


@patch("backend.services.extract_color.rgb_to_hex", return_value="#FFFFFF")
def test_extract_colors_sucesso(mock_rgb_to_hex):
    pixels = np.ones((100, 3), dtype=np.uint8) * 255
    n_colors = 3

    resultado = extract_colors(pixels, n_colors=n_colors)

    assert isinstance(resultado, list)
    assert len(resultado) <= n_colors
    assert "rgb" in resultado[0]
    assert "hex" in resultado[0]
    assert resultado[0]["hex"] == "#FFFFFF"

def test_append_palette_to_image_sucesso():
    imagem_original = np.zeros((100, 100, 3), dtype=np.uint8)
    
    paleta_ficticia = [
        {"rgb": [255, 0, 0], "hex": "#FF0000"},
        {"rgb": [0, 255, 0], "hex": "#00FF00"}
    ]
    
    resultado = append_palette_to_image(imagem_original, paleta_ficticia, n_colors=2)

    assert resultado.shape == (110, 100, 3)
    assert isinstance(resultado, np.ndarray)

@patch("backend.services.palette_pipeline.resize_image")
@patch("backend.services.palette_pipeline.image_to_pixels")
@patch("backend.services.palette_pipeline.extract_colors")
@patch("backend.services.palette_pipeline.append_palette_to_image")
@patch("backend.services.palette_pipeline.image_to_png_bytes")
def test_process_palette_fluxo(
    mock_to_png, mock_append, mock_extract, mock_pixels, mock_resize
):
    mock_resize.return_value = "imagem_redimensionada"
    mock_pixels.return_value = "pixels_da_imagem"
    mock_extract.return_value = [{"rgb": [0, 0, 0], "hex": "#000000"}]
    mock_append.return_value = "imagem_com_paleta"
    mock_to_png.return_value = b"bytes_do_png"

    imagem_input = np.zeros((50, 50, 3), dtype=np.uint8)
    
    paleta, png_bytes = process_palette(imagem_input, n_colors=5)

    mock_resize.assert_called_once_with(imagem_input)
    mock_pixels.assert_called_once_with("imagem_redimensionada")
    mock_extract.assert_called_once_with("pixels_da_imagem", 5)
    mock_append.assert_called_once_with(imagem_input, paleta, 5)
    mock_to_png.assert_called_once_with("imagem_com_paleta")

    assert paleta == [{"rgb": [0, 0, 0], "hex": "#000000"}]
    assert png_bytes == b"bytes_do_png"