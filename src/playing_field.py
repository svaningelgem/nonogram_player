import logging
from dataclasses import dataclass, field
from functools import cached_property
from typing import List

import numpy as np

from .exceptions import CannotSolve, NoSimilaritiesFound, NotMatchingChars
from .grid import Grid
from .image2grid import Image2Grid
from .interpret_number import InterpretNumber
from .line import Line
from .solver_common_line_fields import CommonLineFields
from .solver_line_possibilties import LinePossibilityGenerator
from .utils import ImageType, convert_image_to_numpy, save, split_in_separate_numbers, unknown

logger = logging.getLogger(__name__)


def _get_line_horizontal(solution, idx):
    return solution[idx]


def _set_line_horizontal(solution, idx, value):
    solution[idx] = value


def _get_line_vertical(solution, idx):
    return solution[:, idx]


def _set_line_vertical(solution, idx, value):
    solution[:, idx] = value


@dataclass
class PlayingField:
    """
    Takes in an image, and solves it.
    """

    image: ImageType = field(repr=False)
    iteration: int = 0

    def __post_init__(self):
        self.image = convert_image_to_numpy(self.image)

    def _get_interpreted_numbers(self, sidebar: List[List[np.ndarray]]):
        return [
            [
                int(
                    "".join(
                        InterpretNumber(additional_number, iteration=self.iteration).most_likely
                        for additional_number in split_in_separate_numbers(nr_img)
                    )
                )
                for nr_img in nr_tab
            ]
            for nr_tab in sidebar
        ]

    def _solve_generic(self, solution: np.ndarray, numbers: List[List[int]], horizontal: bool):
        get_line = _get_line_horizontal if horizontal else _get_line_vertical
        set_line = _set_line_horizontal if horizontal else _set_line_vertical

        for line_idx, nrs in enumerate(numbers):
            current_line = get_line(solution, line_idx)
            if np.all(current_line != unknown):
                continue

            current_line = Line(current_line)
            grid_size = len(numbers)
            common_fields = CommonLineFields()

            try:
                for possibility in LinePossibilityGenerator(grid_size, nrs):
                    try:
                        current_line.can_merge(possibility)
                    except NotMatchingChars:
                        continue

                    common_fields.intersect(possibility)

            except NoSimilaritiesFound:
                continue

            current_line.merge(common_fields.line)
            set_line(solution, line_idx, current_line)

    @cached_property
    def grid(self) -> Grid:
        return Image2Grid(self.image).grid

    @property
    def left(self) -> List[List[int]]:
        return self._get_interpreted_numbers(self.grid.left.nr_imgs)

    @property
    def top(self) -> List[List[int]]:
        return self._get_interpreted_numbers(self.grid.top.nr_imgs)

    def _solve(self) -> np.ndarray:
        """
        Main thing that binds all the steps together.
        """
        solution = np.zeros(shape=(len(self.left), len(self.top)), dtype="int8")

        begin = None
        while begin is None or np.any(begin != solution):
            begin = solution.copy()

            self._solve_generic(solution, self.left, horizontal=True)
            self._solve_generic(solution, self.top, horizontal=False)

            if np.all(solution != unknown):
                return solution  # Ok, solved!
        else:
            raise CannotSolve

    @cached_property
    def solution(self) -> List[List[int]]:
        for i in range(3):  # Max 3 iterations:
            self.iteration = i
            try:
                return self._solve().tolist()
            except AssertionError:
                pass

        logger.error('Failing to solve this!! >> Saved as: %s', save(self.image))


