from PIL import Image, ImageEnhance
from PIL import ImageFilter

from tqdm import tqdm

# import numpy as np
# import cv2

def main():
    source_image = Image.open("resources/example3.jpg").convert('RGB')
    gray = source_image.convert('L')
    
    w, h = gray.size

    w_tmp_1 = 100
    h_tmp_1 = h * w_tmp_1 // w

    count = min(w, h) // 5 // 10
    kernel_size = 3
    rank = 3 * 3 - 2

    print(kernel_size)

    tmp = gray.filter(
        ImageFilter.FIND_EDGES
    )


    for w_tmp in [1000, 500, 100, 50, 30]:
        h_tmp = h * w_tmp // w
        tmp = tmp.filter(ImageFilter.RankFilter(kernel_size, rank))
        tmp = ImageEnhance.Contrast(tmp).enhance(256)
        tmp = tmp.resize(size=[w_tmp, h_tmp])
        tmp = tmp.resize(size=[w, h], resample=Image.Resampling.NEAREST)
        # tmp = ImageEnhance.Contrast(tmp).enhance(127)
        tmp.show()

    # tmp = ImageEnhance.Contrast(tmp).enhance(256)
    tmp = tmp.resize(size=[w, h], resample=Image.Resampling.NEAREST)

        # tmp = ImageEnhance.Contrast(tmp).enhance(2)


    # tmp = ImageEnhance.Contrast(tmp).enhance(256)


    tmp = tmp.resize(size=[w, h], resample=Image.Resampling.NEAREST)

    # got = small.filter(
    #     # ImageFilter.MaxFilter(kernel_size)
    #     ImageFilter.RankFilter(kernel_size, rank)
    # ).resize

    # tmp = ImageEnhance.Contrast(tmp).enhance(256)

    tmp = Image.blend(source_image, tmp.convert('RGB'), alpha=.4)

    tmp.show()
    

if __name__ == "__main__":
    main()