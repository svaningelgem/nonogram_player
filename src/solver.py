from dataclasses import dataclass, field
from itertools import count
from typing import Generator, List, Union

from .interpret_grid import Line, LineSimilarities, NoSpaceLeft, cross, filled


def skip_crosses(line: Line, idx: int) -> int:
    try:
        while line[idx] == cross:
            idx += 1
    except IndexError:
        ...

    return idx


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

    def _expand_spaces(self, line: Line, which_one: int, spaces_left: int, start_index: int = 0) -> Generator[Line, None, None]:
        try:
            se: SpaceExpander = self.inner[which_one * 2]  # This is the one we will enlarge in this recursion
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

            yield from self._expand_spaces(current_line, which_one + 1, spaces_left - spaces, start_index + spaces + nb.length)

        a = 1

    def __iter__(self) -> Generator[Line, None, None]:
        yield from self._expand_spaces(
            Line(self.max_line_length),
            0,
            spaces_left=self.max_line_length - sum(self.nrs)
        )


class Solver:
    def get_sureties(self, line: Line, nrs: List[int]):
        """Returns which fields are certain to be either filled or a cross."""

        box = LineSimilarities()

        def build_line(current_line: Line, start_position: int, nrs_to_place: List[int]):
            tmp = current_line.copy()
            max_spaces_left = len(line) - start_position - sum(nrs_to_place) - (len(nrs_to_place) - 1)
            if max_spaces_left < 0:
                raise NoSpaceLeft

            # put cross where you for sure cannot place anything:
            # 'X X     X ' => '2 2'  -->  So we can change this line into 'XXX     XX'
            if max_spaces_left == 0:
                # Only 1 way to place it --> Do it!
                for nr in nrs_to_place:
                    ...
                return

        start_index = 0
        line_length = len(line)
        number_length = sum(nrs) + len(nrs) - 1  # this is the minimal space needed on this line
        for nr_idx, nr in enumerate(nrs):  # These numbers need to be placed on the line
            # if nr_idx != 0:
            #     start_index += 1  # 1 cross at least
            start_index = skip_crosses(line, start_index)







        surely_filled = sum(nrs)  # How many 'filled' there are in this line
        need_at_least_x_spaces = len(nrs) - 1  # How many spaces I need to keep to separate stuff
        if (
                surely_filled + need_at_least_x_spaces == line.len_no_cross_at_end  # "4 5" on a 10 grid, or "8" when there are 2 crosses at the end
                or surely_filled == line.len_no_crosses  # there are already some crosses on the line, and we can nicely fill them
        ):
            ...

