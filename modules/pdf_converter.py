# modules/pdf_converter.py
from pdf2image import convert_from_path
import os

def convert_pdf_to_images(pdf_path, dpi=300):
    """Конвертирует PDF в список изображений PIL"""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF файл не найден: {pdf_path}")
    
    print(f"Конвертируем {pdf_path} в изображения с DPI={dpi}...")
    try:
        images = convert_from_path(pdf_path, dpi=dpi)
        print(f"Успешно загружено {len(images)} страниц.")
        return images
    except Exception as e:
        raise RuntimeError(f"Ошибка при конвертации PDF: {e}")