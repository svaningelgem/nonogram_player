from dataclasses import dataclass
from itertools import count
from typing import Generator, List, Union

from src.line import Line
from src.utils import cross, filled


@dataclass
class SpaceExpander:
    minimal_length: int = 0

    def __iter__(self):
        yield from count(start=self.minimal_length)


@dataclass
class NumberBlock:
    length: int


class LinePossibilityGenerator:
    def __init__(self, max_line_length: int, nrs: List[int]):
        self.max_line_length = max_line_length
        self.nrs = nrs
        self.inner = self._setup()
        self.spaces_left = max_line_length - sum(nrs)

    def _setup(self) -> List[Union[NumberBlock, SpaceExpander]]:
        tmp = []

        for idx, nr in enumerate(self.nrs):
            minimal_length = 1

            if idx == 0:  # First one
                minimal_length = 0

            tmp.append(SpaceExpander(minimal_length=minimal_length))
            tmp.append(NumberBlock(nr))

        return tmp

    def _expand_spaces(
        self, line: Line, which_one: int, spaces_left: int, start_index: int = 0
    ) -> Generator[Line, None, None]:
        try:
            se: SpaceExpander = self.inner[
                which_one * 2
            ]  # This is the one we will enlarge in this recursion
        except IndexError:
            yield line.fill_unknown_with_cross()
            return

        for spaces in se:
            if spaces > spaces_left:
                return

            # Create the line
            current_line = line.copy()
            # Add the spaces we want to add
            for idx in range(spaces):
                try:
                    current_line[start_index + idx] = cross
                except IndexError:
                    return

            # And add the numberblock
            nb: NumberBlock = self.inner[which_one * 2 + 1]
            for idx in range(nb.length):
                try:
                    current_line[start_index + spaces + idx] = filled
                except IndexError:
                    return

            yield from self._expand_spaces(
                current_line,
                which_one + 1,
                spaces_left - spaces,
                start_index + spaces + nb.length,
            )

    def __iter__(self) -> Generator[Line, None, None]:
        yield from self._expand_spaces(
            Line(self.max_line_length),
            0,
            spaces_left=self.max_line_length - sum(self.nrs),
        )
