import logging

from PIL import Image


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

SINGLE_IMAGE_PIXELS = 10000


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
