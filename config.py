# config.py
PDF_PATH = "samples/handwritten_scans.pdf"
OUTPUT_DIR = "output"

# Языки: ['ru', 'en'] — можно добавить другие
LANGUAGES = ['ru', 'en']

# Использовать GPU?
GPU = False

# Порог уверенности OCR
OCR_THRESHOLD = 0.25

# DPI для конвертации PDF
PDF_DPI = 300

# Минимальная длина строки для сохранения
MIN_TEXT_LENGTH = 1

# Режим: 'handwritten', 'printed', 'mixed'
MODE = 'mixed'