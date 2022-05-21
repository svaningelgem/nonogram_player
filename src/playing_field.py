from dataclasses import dataclass, field
from functools import cached_property
from typing import List

import numpy as np

from .exceptions import CannotSolve, NoSimilaritiesFound, NotMatchingChars
from .image2grid import Image2Grid
from .interpret_number import InterpretNumber
from .line import Line
from .solver_common_line_fields import CommonLineFields
from .solver_line_possibilties import LinePossibilityGenerator
from .utils import ImageType, convert_image_to_numpy, split_in_separate_numbers, unknown


@dataclass
class PlayingField:
    """
    Takes in an image, and solves it.
    """

    image: ImageType = field(repr=False)

    def __post_init__(self):
        self.image = convert_image_to_numpy(self.image)

    @staticmethod
    def _get_interpreted_numbers(sidebar: List[List[np.ndarray]]):
        return [
            [
                int(
                    "".join(
                        InterpretNumber(additional_number).most_likely
                        for additional_number in split_in_separate_numbers(nr_img)
                    )
                )
                for nr_img in nr_tab
            ]
            for nr_tab in sidebar
        ]

    @staticmethod
    def _solve_generic(
        solution: np.ndarray, sidebar: List[List[int]], horizontal: bool
    ):
        numbers = sidebar

        if horizontal:

            def get_line(idx):
                return solution[idx]

            def set_line(idx, value):
                solution[idx] = value

        else:

            def get_line(idx):
                return solution[:, idx]

            def set_line(idx, value):
                solution[:, idx] = value

        for line_idx, nrs in enumerate(numbers):
            try:
                current_line = get_line(line_idx)
                if np.all(current_line != unknown):
                    continue

                current_line = Line(current_line)

                common_fields = CommonLineFields()

                for possibility in LinePossibilityGenerator(len(numbers), nrs):
                    try:
                        current_line.can_merge(possibility)
                    except NotMatchingChars:
                        continue

                    common_fields.intersect(possibility)
            except NoSimilaritiesFound:
                continue

            current_line.merge(common_fields.line)
            set_line(line_idx, current_line)

    def _solve(self) -> np.ndarray:
        """
        Main thing that binds all the steps together.
        """
        grid = Image2Grid(self.image).grid

        left = self._get_interpreted_numbers(grid.left.nr_imgs)
        top = self._get_interpreted_numbers(grid.top.nr_imgs)

        solution = np.zeros(shape=(len(left), len(top)), dtype="int8")

        begin = None
        while begin is None or np.any(begin != solution):
            begin = solution.copy()

            self._solve_generic(solution, left, horizontal=True)
            self._solve_generic(solution, top, horizontal=False)

            if np.all(solution != unknown):
                return solution  # Ok, solved!
        else:
            raise CannotSolve

    @cached_property
    def solution(self) -> List[List[int]]:
        return self._solve().tolist()
