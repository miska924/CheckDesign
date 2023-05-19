import cv2
import numpy as np
from PIL import Image
from typing import List

from src.criteria.helpers import scale
from src.criteria.helpers import find_contrasting_color


MERGE_THRESHOLD = 0.05

def draw_bounding_rectangles(img, bounding_rectangles):
    for x, y, w, h in bounding_rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)


def calc_grid_alignment(contours: List, width: int, height: int) -> float:
    horizontal_gaps = 0
    vertical_gaps = 0
    total_gaps = 0

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if x > 0:
            horizontal_gaps += 1

        if y > 0:
            vertical_gaps += 1

        if x + w < width:
            horizontal_gaps += 1

        if y + h < height:
            vertical_gaps += 1

        total_gaps += 4

    alignment = (horizontal_gaps + vertical_gaps) / total_gaps
    return alignment

def chebyshev_distance(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    dx = max(abs(x1 - (x2 + w2)), abs((x1 + w1) - x2))
    dy = max(abs(y1 - (y2 + h2)), abs((y1 + h1) - y2))
    return max(dx - w1 - w2, dy - h1 - h2)

def merge_contours(contours, distance_threshold):
    merged_contours = []
    merged_indices = []

    for i, contour1 in enumerate(contours):
        if i in merged_indices:
            continue

        x1, y1, w1, h1 = cv2.boundingRect(contour1)
        candidate_contours = [contour1]

        for j, contour2 in enumerate(contours[i + 1:], i + 1):
            if j in merged_indices:
                continue

            x2, y2, w2, h2 = cv2.boundingRect(contour2)

            if chebyshev_distance((x1, y1, w1, h1), (x2, y2, w2, h2)) <= distance_threshold:
                candidate_contours.append(contour2)
                merged_indices.append(j)

        if candidate_contours:
            merged_contour = np.concatenate(candidate_contours)
            merged_contours.append(merged_contour)

    return merged_contours

def find_grid(pil_image: Image.Image) -> Image.Image:
    cv2_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    gray_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    edges = cv2.Canny(blurred_image, 100, 200)

    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Фильтруем контуры, уровень иерархии которых равен 0
    distance_threshold = MERGE_THRESHOLD * min(cv2_image.shape[:2])

    merged_contours = contours
    while True:
        prev_len = len(merged_contours)
        merged_contours = merge_contours(merged_contours, distance_threshold)
        if prev_len == len(merged_contours):
            break

    contrasting_color = find_contrasting_color(cv2_image)

    for contour in merged_contours:
        x, y, w, h = cv2.boundingRect(contour)
        # draw_bounding_rectangles(cv2_image, [cv2.boundingRect(contour)])
        cv2.rectangle(cv2_image, (x, y), (x + w, y + h), contrasting_color, 2)

    alignment = calc_grid_alignment(merged_contours, cv2_image.shape[1], cv2_image.shape[0])

    # Возвращаем обработанное изображение cv2 в виде PIL.Image
    return alignment, Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))


def tabular(pil_image):
    w_orig, h_orig = pil_image.size
    tmp = scale(pil_image, 100000)

    alignment, result = find_grid(tmp)

    result = result.resize(size=[w_orig, h_orig], resample=Image.Resampling.LANCZOS)
    return alignment, result