from PIL import Image, ImageOps
import pytesseract
import cv2
import numpy as np


def preprocess_image(image: Image.Image):
    # Изменить размер изображения для улучшения распознавания текста
    image = image.resize((image.width * 2, image.height * 2), Image.ANTIALIAS)

    # Преобразовать изображение в оттенки серого
    image = ImageOps.grayscale(image)

    # Преобразовать изображение в массив NumPy для обработки с использованием OpenCV
    img_arr = np.array(image)

    # Удаление шума с помощью размытия
    img_arr = cv2.medianBlur(img_arr, ksize=3)

    # Выполнить адаптивное пороговое значение
    img_arr = cv2.adaptiveThreshold(
        img_arr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 7
    )

    # Вернуть обработанное изображение в виде PIL.Image
    return Image.fromarray(img_arr)

    
def get_text_length(image: Image.Image):
    # Выполнить предварительную обработку изображения (по желанию)
    image = preprocess_image(image)

    # Извлечь текст с изображения
    text = pytesseract.image_to_string(image)

    # Удалить все ненужные символы, такие как пробелы и переносы строк
    text = "".join(text.split())
    print(text)

    # Вернуть длину текста
    return len(text)