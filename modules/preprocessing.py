# modules/preprocessing.py
import cv2
import numpy as np

def remove_lines(image_array, kernel_size=20):
    """Удаляет горизонтальные и вертикальные линии (линовку)"""
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Горизонтальные линии
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, 1))
    detect_horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel)
    horizontal_mask = cv2.dilate(detect_horizontal, horizontal_kernel, iterations=2)

    # Вертикальные линии
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_size))
    detect_vertical = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel)
    vertical_mask = cv2.dilate(detect_vertical, vertical_kernel, iterations=2)

    # Объединяем маски
    lines_mask = cv2.addWeighted(horizontal_mask, 0.5, vertical_mask, 0.5, 0.0)
    lines_mask = cv2.cvtColor(lines_mask, cv2.COLOR_GRAY2BGR)

    # Удаляем линии из исходного изображения
    result = cv2.subtract(image_array, lines_mask)
    return result

def deskew(image_array, max_skew=10):
    """Автоматически выравнивает наклон текста"""
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    gray = cv2.bitwise_not(gray)
    coords = cv2.findNonZero(gray)
    if coords is None or len(coords) < 10:
        return image_array  # нечего выравнивать

    try:
        rect = cv2.minAreaRect(coords)
        angle = rect[-1]
        if angle < -45:
            angle = 90 + angle
        if abs(angle) <= max_skew:
            (h, w) = image_array.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(image_array, M, (w, h), flags=cv2.INTER_CUBIC,
                                     borderMode=cv2.BORDER_REPLICATE)
            return rotated
    except:
        pass
    return image_array

def enhance_contrast(image_array):
    """Улучшает контраст и бинаризует"""
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    return enhanced

def preprocess_page(image_pil):
    """Полная предобработка страницы"""
    img_array = np.array(image_pil)
    
    # Выравнивание
    img_array = deskew(img_array)
    
    # Удаление линовки
    img_array = remove_lines(img_array)
    
    # Улучшение контраста
    img_array = enhance_contrast(img_array)
    
    return img_array