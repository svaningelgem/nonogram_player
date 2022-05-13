from collections import defaultdict
from dataclasses import dataclass, field
from functools import cache, partial
from time import time
from typing import Dict, Iterable, List

import numpy as np
from PIL import ImageDraw, ImageOps
from PIL.Image import Image, fromarray, open as imopen
from multipledispatch import dispatch

from src.read_nr import NumberReader
from src.utils import TLWH, magenta, pure_white, save, tab_background


cross = -1
unknown = 0
filled = 1


@dataclass
class HintTab:
    direction: str
    img: Image

    tabs: List[np.array] = field(default_factory=list)
    nrs: Dict[int, List[np.array]] = field(default_factory=lambda: defaultdict(list))

    def __post_init__(self):
        self.arr = np.array(self.img)


class Line:
    @dispatch(int)
    def __init__(self, len_: int):
        self._inner = [unknown] * len_

    @dispatch(list)
    def __init__(self, fields: List[int]):
        self._inner = list(fields)

    def __len__(self):
        return len(self._inner)

    @staticmethod
    def ltrim(line) -> 'Line':
        line = line.copy()

        # ltrim the list
        while line and line[0] == cross:
            line = line[1:]

        return line

    @staticmethod
    def rtrim(line) -> 'Line':
        line = line.copy()

        # rtrim the list
        while line and line[-1] == cross:
            line = line[-1:]

        return line

    @property
    def len_no_cross_at_end(self) -> int:
        return len(self.ltrim(self.rtrim(self._inner)))

    @property
    def len_no_crosses(self) -> int:
        return sum(1 for x in self._inner if x != cross)

    def copy(self):
        line = Line(1)
        line._inner = self._inner.copy()
        return line

    def __hash__(self):
        return hash(tuple(self._inner))

    def __iter__(self):
        return iter(self._inner)

    def __repr__(self) -> str:
        return str(['x' if x is cross else x for x in self._inner])

    def __eq__(self, other) -> bool:
        return (
            type(self) == type(other)
            and self._inner == other._inner
        )

    def __getitem__(self, index: int) -> int:
        return self._inner[index]

    def __setitem__(self, index: int, value: int) -> None:
        if index >= len(self._inner):
            raise IndexError

        self._inner[index] = value

    def fill_unknown_with_cross(self) -> 'Line':
        return Line([
            x if x != unknown else cross
            for x in self._inner
        ])


class NoSimilaritiesFound(ValueError): ...
class NoSpaceLeft(ValueError): ...


class LineSimilarities:
    def __init__(self):
        self._inner = None

    def __iadd__(self, other: Line):
        assert isinstance(other, Line)

        if self._inner is None:
            self._inner = other
            return

        self._inner = [x if x == y else unknown for x, y in zip(self._inner, other)]
        if all(x == unknown for x in self._inner):
            raise NoSimilaritiesFound

    def __str__(self):
        return str(self._inner)


class InterpretGrid:
    def __init__(self, img: Image):
        self.img = img.copy().convert('RGB')
        self.nr_reader = NumberReader()

    def _get_bars(self, img: Image, *, left=False):
        tab = HintTab(direction='left' if left else 'top', img=img)
        if left:
            line = tab.arr[:,100]
        else:
            line = tab.arr[100,:]

        # Get spaces of (at least 1) white pixel
        space_start = None
        tab_start = 0
        for i, x in enumerate(line):
            if np.all(x == pure_white):
                if space_start is None:
                    tab.tabs.append((tab_start, i))
                space_start = i
            elif space_start is not None:
                tab_start = i
                space_start = None

        # Last one
        tab.tabs.append((tab_start, len(line)))

        return tab

    def _get_tabs(self, *, left=False):
        if left:
            tlwh = TLWH(60, 980, 226, 1089)
        else:
            tlwh = TLWH(299, 698, 1100, 269)

        cropped = self.img.crop(box=(tlwh.x, tlwh.y, tlwh.x + tlwh.w, tlwh.y + tlwh.h))
        # save(cropped)
        return self._get_bars(cropped, left=left)

    def _crop_data(self, *, left=False):
        def column_selection(arr: np.ndarray, start: int, stop: int = None, *, horizontal: bool, w: int = 1):
            if stop is None:
                stop = start + w

            if horizontal:
                return arr[:,start:stop]
            else:
                return arr[start:stop]

        column_selection_horizontal = partial(column_selection, horizontal=True)
        column_selection_vertical = partial(column_selection, horizontal=False)

        if left:
            flood_fill_point = (12, 4)
            h = column_selection_horizontal
            v = column_selection_vertical
        else:
            flood_fill_point = (8, 9)
            v = column_selection_horizontal
            h = column_selection_vertical

        return flood_fill_point, h, v

    def _my_floodfill(self, original: np.ndarray, pt: tuple, threshold: int = 200) -> np.ndarray:
        img = original.copy().astype('int32')

        x, y = pt

        r, g, b = img[x][y]

        mask_r = abs(img[:, :, 0] - r)
        mask_g = abs(img[:, :, 1] - g)
        mask_b = abs(img[:, :, 2] - b)
        mask = mask_r + mask_g + mask_b
        img[mask <= threshold] = 255

        return img.astype('uint8')

    def crop_numbers(self, *, left=False, do_save=False):
        flood_fill_point, hor_selection, ver_selection = self._crop_data(left=left)
        tab_data = self._get_tabs(left=left)

        if len(tab_data.tabs) == 10:  # level 2
            min_width = 15
        elif len(tab_data.tabs) == 15:  # level 3
            min_width = 15
        elif len(tab_data.tabs) == 20:  # level 4
            min_width = 11
        else:
            raise ValueError(f"Can't do this yet! Got {len(tab_data.tabs)} tabs. File saved as: {save(tab_data.img)}.")

        whitened = self._my_floodfill(tab_data.arr, flood_fill_point, 200)
        if do_save: save(whitened)

        for idx, tab in enumerate(tab_data.tabs):
            tmp2 = ver_selection(whitened, *tab)
            if np.all(tmp2 == pure_white):
                raise ValueError("Nothing in this image??")

            tmp2 = fromarray(tmp2)
            mask = ImageOps.invert(tmp2)  # Make white -> black
            image_box = mask.getbbox()

            cropped = tmp2.crop(image_box)

            tmp3 = np.array(cropped)
            nr_start = 0
            col = 0
            max_col = len(tmp3[0]) if left else len(tmp3)
            while col < max_col:
                if np.all(hor_selection(tmp3, col, w=min_width) == pure_white):
                    # End of number!
                    found_nr = hor_selection(tmp3, nr_start, col)
                    found_nr = self.nr_reader.predict(found_nr)
                    tab_data.nrs[idx].append(found_nr)
                    if do_save: save(found_nr, f'nr')
                    # Skip to first col that isn't pure white
                    col += min_width + 1
                    while col < max_col and np.all(hor_selection(tmp3, col) == pure_white):
                        col += 1
                    nr_start = col

                col += 1

            found_nr = hor_selection(tmp3, nr_start, col+1)
            found_nr = self.nr_reader.predict(found_nr)
            tab_data.nrs[idx].append(found_nr)

            if do_save: save(hor_selection(tmp3, nr_start, col+1), 'nr')

        return tab_data

    def interpret(self):
        # left = self.crop_numbers(left=True)
        # top = self.crop_numbers(left=False)

        left = self._get_tabs(left=True)
        left.nrs = {0: [3], 1: [2, 2], 2: [1, 4], 3: [1, 5], 4: [2, 2, 1, 1], 5: [5, 1], 6: [5, 1], 7: [2, 1], 8: [1, 2], 9: [6]}

        top = self._get_tabs(left=False)
        top.nrs = {0: [3, 1], 1: [3, 1], 2: [3, 1], 3: [9], 4: [2, 3, 1], 5: [1, 2, 2], 6: [9], 7: [3], 8: [2], 9: [2]}

        matrix = [
            Line(len(left.nrs))
            for _ in range(len(top.nrs))
        ]



if __name__ == '__main__':
    start = time()
    InterpretGrid(imopen("../screenshots/level2/2022-05-09 140127.png")).interpret()
    stop = time()

    print(f'One run took {stop - start}s')
