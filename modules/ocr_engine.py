# modules/ocr_engine.py
import easyocr

class OCREngine:
    def __init__(self, languages=['en'], gpu=False):
        print("Загружаем модели OCR...")
        self.reader = easyocr.Reader(languages, gpu=gpu)
    
    def recognize(self, image_array, threshold=0.2, min_length=1):
        """Распознаёт текст с обработанного изображения"""
        with open("temp_page.png", "wb") as f:
            f.write(cv2.imencode(".png", image_array)[1].tobytes())
        
        results = self.reader.readtext(
            "temp_page.png",
            detail=1,
            paragraph=False,
            text_threshold=0.7,
            low_text=0.4,
            link_threshold=0.4
        )
        
        # Фильтрация по уверенности и длине
        recognized = []
        for (bbox, text, prob) in results:
            text = text.strip()
            if prob >= threshold and len(text) >= min_length:
                recognized.append({
                    'text': text,
                    'confidence': prob,
                    'bbox': bbox
                })
        return recognized