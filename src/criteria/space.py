from PIL import Image, ImageEnhance, ImageOps, ImageStat, ImageFilter

from criteria.helpers import scale


def space(source: Image):
    w_orig, h_orig = source.size
    area_orig = w_orig * h_orig

    tmp = scale(source)
    w, h = tmp.size

    tmp = tmp.convert("L")
    tmp = tmp.filter(ImageFilter.FIND_EDGES)
    tmp = scale(tmp)
    tmp = tmp.filter(
        ImageFilter.Kernel(
            size=(5, 5),
            kernel=[
                0,
                0.8,
                1,
                0.8,
                0,
                0.8,
                1,
                1,
                1,
                0.8,
                1,
                1,
                1,
                1,
                1,
                0.8,
                1,
                1,
                1,
                0.8,
                0,
                0.8,
                1,
                0.8,
                0,
            ],
        )
    )

    tmp = tmp.resize(size=[w_orig, h_orig], resample=Image.Resampling.LANCZOS)

    tmp = ImageEnhance.Brightness(tmp).enhance(10)
    tmp = ImageEnhance.Contrast(tmp).enhance(256)
    tmp = tmp.filter(ImageFilter.SMOOTH_MORE)
    tmp = ImageOps.invert(tmp)

    return ImageStat.Stat(tmp).mean[0] / 255, Image.blend(
        source, tmp.convert("RGB"), alpha=0.8
    )
