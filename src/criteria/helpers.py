import logging

from PIL import Image
import numpy as np


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

SINGLE_IMAGE_PIXELS = 100000


def scale(source: Image, pixels_count=SINGLE_IMAGE_PIXELS):
    result = source.copy()

    w_orig, h_orig = source.size
    logging.info(f"w_orig, h_orig == {w_orig}, {h_orig}")

    image_pixels_count = w_orig * h_orig

    logging.info(f"image_pixels_count {image_pixels_count}")
    logging.info(
        f"(SINGLE_IMAGE_PIXELS / image_pixels_count) {(pixels_count / image_pixels_count)}"
    )

    w = int(w_orig * (pixels_count / image_pixels_count) ** 0.5)
    h = int(h_orig * (pixels_count / image_pixels_count) ** 0.5)

    logging.info(f"w * h = {w} * {h} = {w * h}")

    result = result.resize(size=[w, h], resample=Image.LINEAR)

    return result

def find_contrasting_color(image: np.ndarray) -> tuple:
    avg_color_per_row = np.average(image, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    contrasting_color = tuple([255 - c for c in avg_color])
    return contrasting_color