import os
from collections import namedtuple
from datetime import datetime
from pathlib import Path
from typing import Union

import numpy as np
from PIL.Image import Image, fromarray


def save(img: Union[Image, np.ndarray], subfolder: str = '') -> Path:
    if subfolder:
        filename = f'../screenshots/{subfolder}/{datetime.now().strftime("%Y-%m-%d %H%M%S")}'
    else:
        filename = f'../screenshots/{datetime.now().strftime("%Y-%m-%d %H%M%S")}'
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


TLWH = namedtuple('TLWH', 'x y w h')
pure_white = (255, 255, 255)
tab_background = (0xeb, 0xef, 0xf7)
magenta = (255, 0, 255)