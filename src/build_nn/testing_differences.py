import json
import operator
import random
from pathlib import Path

import cv2
import numpy as np
from PIL import ImageOps
from PIL.Image import fromarray

from src.build_nn.split_plus10_further import white
from src.utils import scale_image_to_100x100, scale_to_100x100

images_path = Path(__file__).parent / 'images'
test_path = images_path / 'test'
test_path.mkdir(parents=True, exist_ok=True)

images = {
    img.stem: scale_to_100x100(img).astype('int8')
    for img in images_path.glob('*.png')
}

all_other_images = [
    img
    for img in images_path.rglob('*.png')
    if img.parent != images_path
]


def skip_whites(img: np.ndarray, start_row: int = 0) -> int:
    while start_row < len(img):
        if not np.all(img[:, start_row] == white):
            break

        start_row += 1

    return start_row


def _test_one_image(img):
    # Read in the file
    src = scale_to_100x100(img).astype('int8')

    # And compare it against the others
    white_pixels = {}
    for j, (nr, arr) in enumerate(images.items()):
        diff = src - arr

        white_pixels[nr] = np.count_nonzero(diff == 0)

    final_conclusion = sorted(white_pixels.items(), key=lambda x: x[1], reverse=True)

    if final_conclusion[0][0] != img.parent.name:
        # Copy test file
        i = img.parent.name
        tgt = test_path / f'{i}.png'
        tgt.write_bytes(img.read_bytes())

        for nr, arr in images.items():
            tgt = test_path / f'{i}_compare_against_{nr}.png'

            diff = src - arr
            cv2.imwrite(str(tgt), diff.astype('uint8'))

        (test_path / 'white_pixels.txt').write_text(json.dumps(dict(final_conclusion), indent=4))

        raise AssertionError(f'{img} failed the test ({dict(final_conclusion)}).')


def test_1():
    # some_test = random.sample(all_other_images, 10)
    for img in all_other_images:
        _test_one_image(img)
