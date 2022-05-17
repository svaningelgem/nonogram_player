from pathlib import Path

import cv2
import numpy as np
from easyocr import Reader

# initialize the reader object
from src.utils import scale_to_100x100

reader = Reader(['en'])

images_path = Path(__file__).parent / 'images'
test_path = images_path / 'test'
test_path.mkdir(parents=True, exist_ok=True)


images = {
    img.stem: scale_to_100x100(img)
    for img in images_path.glob('*.png')
}

all_other_images = [
    img
    for img in images_path.rglob('*.png')
    if img.parent != images_path
]


def test_1():
    # some_test = random.sample(all_other_images, 10)
    kernel = np.ones((5,5), np.uint8)
    args = dict(
        allowlist=list('0123456789'),
        detail=1,
        # text_threshold=0.3,
        # decoder='wordbeamsearch',
        # batch_size=10,
        mag_ratio=2.0,
    )

    for img in all_other_images:
        if img.parent.name in ['0']:
            continue
        if img.name != '86.png':
            continue

        nr = scale_to_100x100(img)

        detection = reader.readtext(nr, **args)
        if not detection:  # Add border & try again
            def add_border(img, size):
                tmp = np.full((img.shape[0] + size*2, img.shape[1] + size*2), 255, dtype=img.dtype)
                tmp[size:img.shape[0] + size, size:img.shape[1] + size] = img
                return tmp

            detection = reader.readtext(add_border(nr, 10), **args)


        assert len(detection) == 1, f"Can't detect anything in {img}."
        bbox, nr_found, confidence = detection[0]
        if nr_found.lower() == 'o':
            nr_found = '0'
        assert nr_found == img.parent.name, f'Failed on {img} --> {detection}.'
