import json
from dataclasses import InitVar, dataclass, field
from functools import cache, cached_property
from math import sqrt
from pathlib import Path
from typing import Dict, List, Tuple, Union

import cv2
import numpy as np
from easyocr import Reader
from numpy.linalg import norm

from src.build_nn.split_plus10_further import white
from src.utils import save, scale_to_100x100

images_path = Path(__file__).parent / 'images'
test_path = images_path / 'test'
test_path.mkdir(parents=True, exist_ok=True)


def extract_pure_image(img):
    tmp = scale_to_100x100(img).astype('int8')
    tmp[tmp > 0] = 127
    tmp[tmp < 0] = -1
    return tmp


images = {
    img.stem: extract_pure_image(img)
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


@dataclass
class ComparisonForOne:
    _background: np.ndarray = field(repr=False)
    _foreground: np.ndarray = field(repr=False)
    back_white_pixels: int = 0
    fore_white_pixels: int = 0
    same_white_pixels: int = 0

    def __post_init__(self):
        self.back_white_pixels = np.count_nonzero(self._background == -1)
        self.fore_white_pixels = np.count_nonzero(self._foreground == -1)
        self.same_white_pixels = np.count_nonzero((self._foreground == -1) & (self._background == -1))

    @property
    def distance(self):
        f = self.fore_white_pixels - self.same_white_pixels
        b = self.back_white_pixels - self.same_white_pixels

        return sqrt(f**2 + b**2)

    @cached_property
    def diff(self):
        return self._background - self._foreground

    @cached_property
    def eq(self):
        return np.count_nonzero(self.diff == 0)


@dataclass
class Comparison:
    img: Union[str, Path]

    _src: np.ndarray = field(repr=False, default=None)
    _src_white_pixels: int = 0
    _comparison: Dict[str, ComparisonForOne] = field(default_factory=dict)
    _dilated: Dict[str, ComparisonForOne] = field(default_factory=dict)
    _eroded: Dict[str, ComparisonForOne] = field(default_factory=dict)

    def __post_init__(self):
        self._src = extract_pure_image(self.img)
        self._src_white_pixels = np.count_nonzero(self._src == -1)

        kernel = np.ones((5, 5), 'uint8')
        self.dilated = cv2.dilate(self._src.astype('uint8'), kernel, iterations=1).astype('int8')
        self.eroded = cv2.erode(self._src.astype('uint8'), kernel, iterations=1).astype('int8')

        for nr, arr in images.items():
            self._comparison[nr] = ComparisonForOne(self._src, arr)
            self._dilated[nr] = ComparisonForOne(
                self.dilated,
                cv2.dilate(arr.astype('uint8'), kernel, iterations=1).astype('int8')
            )
            self._eroded[nr] = ComparisonForOne(
                self.eroded,
                cv2.erode(arr.astype('uint8'), kernel, iterations=1).astype('int8')
            )

    def _preds(self, for_this, do_this = lambda x: x.eq):
        dct = {
            nr: do_this(comp)
            for nr, comp in for_this.items()
        }

        return sorted(dct.items(), key=lambda x: x[1], reverse=True)

    @cached_property
    def preds(self):
        return self._preds(self._comparison)

    @cached_property
    def preds_dilated(self):
        return self._preds(self._dilated)

    @cached_property
    def preds_eroded(self):
        return self._preds(self._eroded)

    @cached_property
    def confidence(self):
        worst = max(x.distance for x in self._comparison.values())

        return self._preds(self._comparison, lambda v: 1 - (v.distance / worst))


ocr = None


def _add_border(img, size):
    tmp = np.full((img.shape[0] + size*2, img.shape[1] + size*2), 255, dtype=img.dtype)
    tmp[size:img.shape[0] + size, size:img.shape[1] + size] = img
    return tmp


def detect_via_ocr(comp: Comparison) -> Tuple[str, float]:
    global ocr
    if ocr is None:
        ocr = Reader(['en', 'nl'])

    args = dict(allowlist=list('0123456789'), detail=1)

    for detect_via in ['normal', 'dilated', 'eroded']:
        if detect_via == 'normal':
            work = comp._src
        elif detect_via == 'dilated':
            work = comp.dilated
        elif detect_via == 'eroded':
            work = comp.eroded
        else:
            raise ValueError

        work = work.copy().astype('uint8')
        detection = ocr.readtext(work, **args)
        if detection:
            break

        # Add border & try again
        detection = ocr.readtext(_add_border(work, 10).astype('uint8'), **args)
        if detection:
            break
    else:
        return []

    return detection[0][1:]  # nr + confidence


def _say_which_letter(img: Union[str, Path]) -> str:
    comp = Comparison(img)

    # Too little difference between the first 2. --> I'm not sure this is the right one then!
    if comp.confidence[0][1] - comp.confidence[1][1] < 0.05:
        ocr_detection = detect_via_ocr(comp)
        if ocr_detection:
            return ocr_detection[0]
        a = 1

    return comp.confidence[0][0]

    # print('')
    # print(img)
    # print(f'- {comp.preds}')
    # print(f'- {comp.preds_dilated}')
    # print(f'- {comp.preds_eroded}')
    # print(f'- {comp.confidence}')
    # print('-', detect_via_ocr(comp))


def test_1():
    # some_test = random.sample(all_other_images, 10)
    for img in all_other_images:
        assert _say_which_letter(img) == img.parent.name


def test_2():
    # _test_one_image(r'E:\nonogram_player\src\build_nn\images\2\2193.png')
    # _test_one_image(r'E:\nonogram_player\src\build_nn\images\8\1002.png')
    # _test_one_image(r'E:\nonogram_player\src\build_nn\images\1\86.png')
    # _test_one_image(r'E:\nonogram_player\src\build_nn\images\5\2222.png')
    _test_one_image(r'E:\nonogram_player\src\build_nn\images\1.png')


def test_3():
    tmp = images['0']
    cv2.imwrite(str(test_path / 'out.png'), tmp)
    cv2.imwrite(str(test_path / 'out_plus_1.png'), tmp + 1)
    tmp[tmp > 0] = 127
    tmp[tmp < 0] = -1
    cv2.imwrite(str(test_path / 'out_fix.png'), tmp)
