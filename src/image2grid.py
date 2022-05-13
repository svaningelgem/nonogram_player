from functools import cached_property, partial
from typing import Dict, List

import numpy as np
from PIL import ImageOps
from PIL.Image import Image, fromarray

from src.hint_tab import HintTab
from src.grid import Grid
from src.read_nr import NumberReader
from src.utils import TLWH, pure_white, save


class Image2Grid:
    def __init__(self, img: Image):
        self.img = img.copy().convert('RGB')
        self.nr_reader = NumberReader()
        self.tabs_left = self.tabs_top = None

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
                    tab.shapes.append((tab_start, i))
                space_start = i
            elif space_start is not None:
                tab_start = i
                space_start = None

        # Last one
        tab.shapes.append((tab_start, len(line)))
        tab.nr_imgs = [list() for _ in range(len(tab))]
        tab.nrs = [list() for _ in range(len(tab))]

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

    def crop_numbers(self, *, left: bool = False, do_save: bool = False) -> List[List[int]]:
        flood_fill_point, hor_selection, ver_selection = self._crop_data(left=left)
        tab_data = self._get_tabs(left=left)
        if left:
            self.tabs_left = tab_data
        else:
            self.tabs_top = tab_data

        if len(tab_data) == 10:  # level 2
            min_width = 15
        elif len(tab_data) == 15:  # level 3
            min_width = 15
        elif len(tab_data) == 20:  # level 4
            min_width = 11
        else:
            raise ValueError(f"Can't do this yet! Got {len(tab_data)} tabs. File saved as: {save(tab_data.img)}.")

        whitened = self._my_floodfill(tab_data.arr, flood_fill_point, 200)
        if do_save: save(whitened)

        for idx, tab in enumerate(tab_data.shapes):
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
                    found_nr_img = hor_selection(tmp3, nr_start, col)
                    tab_data.nr_imgs[idx].append(found_nr_img)
                    found_nr = self.nr_reader.predict(found_nr_img)
                    tab_data.nrs[idx].append(found_nr)
                    if do_save: save(found_nr_img, f'nr')
                    # Skip to first col that isn't pure white
                    col += min_width + 1
                    while col < max_col and np.all(hor_selection(tmp3, col) == pure_white):
                        col += 1
                    nr_start = col

                col += 1

            found_nr_img = hor_selection(tmp3, nr_start, col+1)
            tab_data.nr_imgs[idx].append(found_nr_img)
            found_nr = self.nr_reader.predict(found_nr_img)
            tab_data.nrs[idx].append(found_nr)
            if do_save: save(found_nr_img, f'nr')

            if do_save: save(hor_selection(tmp3, nr_start, col+1), 'nr')

        return tab_data.nrs

    @cached_property
    def grid(self):
        return Grid(
            left=self.crop_numbers(left=True),
            top=self.crop_numbers(left=False),
        )
