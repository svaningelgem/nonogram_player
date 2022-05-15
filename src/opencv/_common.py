import cv2
import numpy as np
import pandas as pd

from functools import cache
from pathlib import Path
from typing import Union


from pathlib import Path

from src.common import natural_sort

base_path = Path(r'E:\nonogram_player\screenshots\nr')
all_files = natural_sort(base_path.rglob('*.png'))


@cache
def scale_to_100x100(img_path: Union[Path, str]) -> np.ndarray:
    """
    - Open the image
    - enlarge the canvas to the maximum dimension
    - rescale to 100x100
    - convert to grayscale
    """
    original_image = cv2.imread(str(img_path))
    im = original_image

    max_ = max(im.shape[:2])

    background = np.zeros(shape=(max_, max_, 3), dtype=np.uint8)
    background[:] = (255, 255, 255)

    center_x = (max_ - im.shape[0]) // 2
    center_y = (max_ - im.shape[1]) // 2

    background[center_x:center_x+im.shape[0], center_y:center_y+im.shape[1]] = im

    # save(background)

    new_img = cv2.resize(background, dsize=(100, 100), interpolation=cv2.INTER_LINEAR)
    # save(new_img)

    return cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)

