from PIL import Image, ImageEnhance, ImageFilter

import matplotlib.pyplot as plt
import logging

from criteria.helpers import scale

TREASHOLD = 5
EPS = 0.8


def tabular(source: Image):
    w_orig, h_orig = source.size

    tmp = scale(source)
    w, h = tmp.size

    tmp = tmp.copy().convert("L")
    logging.info(tmp.size)
    tmp = tmp.filter(ImageFilter.FIND_EDGES)

    logging.info(tmp.size)
    tmp = ImageEnhance.Contrast(tmp).enhance(256)
    logging.info(tmp.size)

    res = Image.new(mode="L", size=tmp.size, color="black")

    tmp_tmp = tmp.resize([1, h], resample=Image.BICUBIC)
    contrasts = [tmp_tmp.getpixel((0, x)) for x in range(h)]

    left_tabular = None
    for i, value in enumerate(contrasts):
        if i > 0 and value > TREASHOLD:
            left_tabular = i
            for x in range(w):
                res.putpixel((x, left_tabular), 255)
            break

    right_tabular = None
    for i, value in enumerate(reversed(contrasts)):
        if i > 0 and value > TREASHOLD:
            right_tabular = i
            for x in range(w):
                res.putpixel((x, h - right_tabular - 1), 255)
            break

    tmp_tmp = tmp.resize([w, 1], resample=Image.LINEAR)
    contrasts = [tmp_tmp.getpixel((x, 0)) for x in range(w)]

    up_tabular = None
    for i, value in enumerate(contrasts):
        if i > 0 and value > TREASHOLD:
            up_tabular = i
            for y in range(h):
                res.putpixel((up_tabular, y), 255)
            break

    down_tabular = None
    for i, value in enumerate(reversed(contrasts)):
        if i > 0 and value > TREASHOLD:
            down_tabular = i
            for y in range(h):
                res.putpixel((w - down_tabular - 1, y), 255)
            break

    tmp = res

    tmp = tmp.resize(size=[w_orig, h_orig], resample=Image.Resampling.NEAREST)

    left_tabular += 1
    right_tabular += 1
    up_tabular += 1
    down_tabular += 1

    tabular_status = (
        (left_tabular / up_tabular > EPS and up_tabular / left_tabular > EPS)
        + (right_tabular / up_tabular > EPS and up_tabular / right_tabular > EPS)
        + (left_tabular / down_tabular > EPS and down_tabular / left_tabular > EPS)
        + (right_tabular / down_tabular > EPS and down_tabular / right_tabular > EPS)
    )

    logging.info(left_tabular)
    logging.info(right_tabular)
    logging.info(up_tabular)
    logging.info(down_tabular)
    logging.info(f"tabular_ok == {tabular_status}")

    return tabular_status, tmp.convert("RGB")
