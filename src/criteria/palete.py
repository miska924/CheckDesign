from PIL import Image
from sklearn.cluster import KMeans
import numpy as np


def find_main_colors(pil_image: Image.Image) -> Image.Image:
    pil_image = pil_image.convert('RGB')
    num_colors = 3

    img_data = np.array(pil_image).reshape(-1, 3)
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(img_data)

    main_colors = [tuple(map(int, centroid)) for centroid in kmeans.cluster_centers_]

    new_width = pil_image.width
    new_height = pil_image.height

    new_image = Image.new('RGB', (new_width, new_height))

    square_width = new_width // 3

    for i in range(num_colors):
        color = main_colors[i]
        square = Image.new('RGB', (square_width, new_height), color)
        new_image.paste(square, (i * square_width, 0))

    return new_image