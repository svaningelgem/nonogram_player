from dataclasses import dataclass
from typing import Dict, List

import numpy as np

from src.common import unknown
from src.exceptions import CannotSolve, FullySolved, NoSimilaritiesFound, NotMatchingChars
from src.hint_tab import HintTab
from src.line import Line
from src.solver_common_line_fields import CommonLineFields
from src.solver_line_possibilties import LinePossibilityGenerator


@dataclass
class Grid:
    left: HintTab
    top: HintTab

    def __post_init__(self):
        self.inner = np.zeros(shape=(len(self.left), len(self.top)), dtype='int8')

    def _solve_generic(self, horizontal: bool):
        if horizontal:
            numbers = self.left

            def get_line(idx):
                return self.inner[idx]

            def set_line(idx, value):
                self.inner[idx] = value
        else:
            numbers = self.top

            def get_line(idx):
                return self.inner[:, idx]

            def set_line(idx, value):
                self.inner[:, idx] = value

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

    def solve(self):
        begin = None
        while begin is None or np.any(begin != self.inner):
            begin = self.inner.copy()

            self._solve_generic(horizontal=True)
            self._solve_generic(horizontal=False)

            if np.all(self.inner != unknown):
                break  # Ok, solved!
        else:
            raise CannotSolve
