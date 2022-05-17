import hashlib
import os
from collections import defaultdict, namedtuple
from datetime import datetime
from functools import cache
from pathlib import Path
from typing import Dict, List, Union

import cv2
import numpy as np
from PIL import ImageOps
from PIL.Image import Image, fromarray

from src.common import natural_sort


screenshots_path = Path(__file__).parent / '../screenshots'
screenshots_levels_path = screenshots_path / 'levels'
processed_path = screenshots_path / 'processed'
numbers_path = screenshots_path / 'new_nr'
final_numbers_path = screenshots_path / 'nr'

all_final_number_files = natural_sort(final_numbers_path.rglob('*.png'))

for x in [x for x in globals().values()]:
    if isinstance(x, Path):
        x.mkdir(parents=True, exist_ok=True)


counter = 0

TLWH = namedtuple('TLWH', 'x y w h')
pure_white = (255, 255, 255)
tab_background = (0xeb, 0xef, 0xf7)
magenta = (255, 0, 255)


def save(img: Union[Image, np.ndarray], subfolder: str = '', *, increasing: bool = False) -> Path:
    if subfolder:
        filename = Path(__file__).parent / f'../screenshots/{subfolder}/{datetime.now().strftime("%Y-%m-%d %H%M%S")}'
    else:
        filename = Path(__file__).parent / f'../screenshots/{datetime.now().strftime("%Y-%m-%d %H%M%S")}'

    if increasing:
        global counter
        filename = filename.parent / f'{counter}.png'
        counter += 1
        target = filename
    else:
        filename = str(filename)
        nr = ''
        n = 0
        ext = '.png'
        while os.path.exists(filename + nr + ext):
            n += 1
            nr = f'_{n}'

        target = Path(filename + nr + ext)

    target.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(img, np.ndarray):
        img = fromarray(img)

    img.save(str(target))

    return target


def remove_duplicate_images(from_path: Path) -> None:
    hashes: Dict[str, List[Path]] = defaultdict(list)
    for file in from_path.rglob('*.png'):
        hashes[md5hash(file)].append(file)

    for hsh, file_list in hashes.items():
        for file in natural_sort(file_list)[1:]:
            print('Removing duplicate', file)
            file.unlink()


@cache
def md5hash(file: Union[str, Path]) -> str:
    return hashlib.md5(Path(file).read_bytes()).hexdigest()


@cache
def is_same_file(file1: Union[str, Path], file2: Union[str, Path]) -> bool:
    return md5hash(file1) == md5hash(file2)


def scale_image_to_100x100(original_image: np.ndarray) -> np.ndarray:
    """
    - enlarge the canvas to the maximum dimension
    - rescale to 100x100
    """

    # Crop it first
    tmp = fromarray(original_image)
    mask = ImageOps.invert(tmp)  # Make white -> black
    image_box = mask.getbbox()
    cropped = tmp.crop(image_box)

    # Now resize it to 100x100
    im = np.array(cropped)

    max_ = max(im.shape[:2])

    # make a max_ by max_ image
    background = np.zeros(shape=(max_, max_, 3), dtype=original_image.dtype)
    # Set the background to white
    background[:] = (255, 255, 255)

    # Find the center
    center_x = (max_ - im.shape[0]) // 2
    center_y = (max_ - im.shape[1]) // 2

    # And paste the original image on it.
    background[center_x:center_x+im.shape[0], center_y:center_y+im.shape[1]] = im

    # save(background)

    # And now resize the image from (max, max) -> (100, 100)
    new_img = cv2.resize(background, dsize=(100, 100), interpolation=cv2.INTER_NEAREST)
    # save(new_img)

    return new_img


@cache
def scale_to_100x100(img_path: Union[Path, str]) -> np.ndarray:
    """
    - Open the image
    - enlarge the canvas to the maximum dimension
    - rescale to 100x100
    - convert to grayscale
    """
    image = cv2.imread(str(img_path))
    new_img = scale_image_to_100x100(image)
    return cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
