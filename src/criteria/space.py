from PIL import Image, ImageEnhance, ImageOps, ImageStat, ImageFilter
import cv2
import numpy as np

from src.criteria.helpers import scale


def space(source: Image):
    w_orig, h_orig = source.size

    tmp = scale(source, 100000)
    
    space, tmp = highlight_air(tmp)

    tmp = tmp.resize(size=[w_orig, h_orig], resample=Image.Resampling.LANCZOS)

    return space, tmp

def find_expanded_edges(image: np.ndarray, min_dim: int) -> np.ndarray:
    edges = cv2.Canny(image, 100, 200)
    kernel_size = max(min_dim // 50, 1) * 2 + 1
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel)

    return dilated_edges

def calculate_air(image: Image.Image):
    cv2_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray_image, cv2.CV_32F, ksize=5)

    threshold = (np.max(laplacian) - np.min(laplacian)) * 0.1
    air_mask = (laplacian < threshold).astype(np.uint8) * 255

    min_dim = min(cv2_image.shape[:2])
    dilated_edges = find_expanded_edges(gray_image, min_dim)
    air_mask[dilated_edges > 0] = 0

    air_ratio = np.sum(air_mask) / (air_mask.shape[0] * air_mask.shape[1] * 255)
    return air_ratio, air_mask

def highlight_air(pil_image: Image.Image):
    air_ratio, air_mask = calculate_air(pil_image)

    air_mask_colored = cv2.cvtColor(air_mask, cv2.COLOR_GRAY2BGR)
    cv2_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    highlighted_image = cv2.addWeighted(cv2_image, 0.5, air_mask_colored, 0.5, 0)

    return air_ratio, Image.fromarray(cv2.cvtColor(highlighted_image, cv2.COLOR_BGR2RGB))