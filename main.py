# main.py
from config import *
from modules.pdf_converter import convert_pdf_to_images
from modules.preprocessing import preprocess_page
from modules.ocr_engine import OCREngine
from modules.exporter import save_as_txt, save_as_docx
import os
import cv2

def main():
    # Создаём папку для вывода
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    txt_path = os.path.join(OUTPUT_DIR, "recognized.txt")
    docx_path = os.path.join(OUTPUT_DIR, "recognized.docx")

    # Конвертация PDF → изображения
    try:
        pages = convert_pdf_to_images(PDF_PATH, dpi=PDF_DPI)
    except Exception as e:
        print("❌ Ошибка при загрузке PDF:", e)
        return

    # Инициализация OCR
    ocr = OCREngine(languages=LANGUAGES, gpu=GPU)

    # Хранилище результатов
    all_results = []

    # Обработка каждой страницы
    for page_num, pil_image in enumerate(pages, 1):
        print(f"\n🔄 Обработка страницы {page_num}...")
        
        # Предобработка
        processed = preprocess_page(pil_image)
        
        # OCR
        result = ocr.recognize(processed, threshold=OCR_THRESHOLD, min_length=MIN_TEXT_LENGTH)
        all_results.append(result)
        
        print(f"  Найдено строк: {len(result)}")

    # Экспорт
    save_as_txt(all_results, txt_path)
    save_as_docx(all_results, docx_path)

    print("\n✅ Обработка завершена!")
    print(f"Результаты в папке: ./{OUTPUT_DIR}/")

if __name__ == "__main__":
    main()