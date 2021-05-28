import os
import random

import numpy as np
from skimage import io
from sklearn.cluster import KMeans

from PIL import Image, ImageDraw

def path(file_name):
    return f'{folder}/{file_name}'


def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def write_to_png(colors, block_size=30):
    length = len(colors) * int(block_size)
    height = int(block_size)
    color_blocks = Image.new('RGB', (length, height), (0, 0, 0))

    image_draw = ImageDraw.Draw(color_blocks, 'RGB')
    pix = color_blocks.load()
    for i in range(len(colors)):
        x = i * block_size
        image_draw.polygon([(x, 0), (x, block_size), (x + block_size, block_size), (x + block_size, 0)],
                           fill=tuple(colors[i].astype('uint8')))

    return color_blocks


def create_image():
    original = io.imread('/home/daniel/PycharmProjects/paintler/me.JPG')



    global folder
    folder = str(random.randint(0, 10000))
    os.mkdir(folder)
    os.chmod(folder, 0o777)

    for n_colors in range(10, 11):
        i = Image.fromarray(original.astype('uint8'), 'RGB')
        dithered = i.convert(mode='P', colors=16, dither=1)
        dithered.save(path('d.jpg'))
        org = io.imread(f'/home/daniel/PycharmProjects/paintler/{path("d.jpg")}')

        arr = org.reshape((-1, 3))
        kmeans = KMeans(n_clusters=n_colors, random_state=42).fit(arr)
        labels = kmeans.labels_
        centers = kmeans.cluster_centers_
        less_colors = centers[labels].reshape(org.shape).astype('uint8')



        create_color_highlights(less_colors, centers)
        color_blocks = write_to_png(centers, block_size=round(less_colors.shape[1] / n_colors))
        simple_image = Image.fromarray(less_colors.astype('uint8'), 'RGB')
        x = get_concat_v(simple_image, color_blocks)
        x.save(path(f'p{n_colors}.png'))
        print(f"p{n_colors}.png created!")


def create_color_highlights(less_colors, colors):
    zeros = {tuple(colors[i].astype('uint8')): np.zeros(less_colors.shape) for i in range(len(colors))}
    for i, x in enumerate(less_colors):
        for j, y in enumerate(x):
            zeros[tuple(y)][i][j] = y
            pass

    for i in range(len(colors)):
        Image.fromarray(list(zeros.values())[i].astype('uint8')).save(path(f"c{i}c_{str(colors.astype('uint8')[0])[1:-1].replace(' ', '_')}.png"))


create_image()
