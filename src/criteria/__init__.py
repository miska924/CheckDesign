import logging

from PIL import Image, ImageEnhance, ImageOps, ImageStat, ImageFilter


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def space(source: Image):
    w, h = source.size

    tmp = source.copy().convert('L')
    tmp = tmp.filter(ImageFilter.FIND_EDGES)

    for w_tmp in [1000, 700, 500, 200, 100, 70, 50]:
        tmp = tmp.filter(ImageFilter.MaxFilter(9))
        tmp = ImageEnhance.Contrast(tmp).enhance(256)

        h_tmp = h * w_tmp // w
        tmp = tmp.resize(size=[w_tmp, h_tmp])
        tmp = tmp.resize(size=[w, h], resample=Image.Resampling.LANCZOS)

    tmp = ImageOps.invert(tmp)
    tmp = ImageEnhance.Contrast(tmp).enhance(256)

    return ImageStat.Stat(tmp).mean[0] / 255, Image.blend(source, tmp.convert('RGB'), alpha=.8)

def tabular(source: Image):
    w, h = source.size

    tmp = source.copy().convert('L')
    tmp = tmp.filter(ImageFilter.FIND_EDGES)

    pixels = list(tmp.getdata())

    contrasts = [0]
    max_contrast = 0
    for tab_size in range(1, w - 1):
        contrast = 0
        for x in range(h):
            contrast += abs(tmp.getpixel((tab_size - 1, x)) - tmp.getpixel((tab_size + 1, x)))
        contrast //= h
        max_contrast = max(max_contrast, contrast)
        contrasts.append(contrast)

    tmp2 = tmp.copy()
    for tab_size in range(1, w - 1):
        for x in range(h):
            tmp2.putpixel((tab_size, x), 255 * contrasts[tab_size] // max_contrast)

    contrasts = [0]
    max_contrast = 0
    for tab_size in range(1, h - 1):
        contrast = 0
        for x in range(w):
            contrast += abs(tmp.getpixel((x, tab_size - 1)) - tmp.getpixel((x, tab_size + 1)))
        contrast //= h
        max_contrast = max(max_contrast, contrast)
        contrasts.append(contrast)

    tmp3 = tmp.copy()
    for tab_size in range(1, h - 1):
        for x in range(w):
            tmp3.putpixel((x, tab_size), 255 * contrasts[tab_size] // max_contrast)

    return True, Image.blend(tmp2, tmp3, alpha=.5).convert("RGB")