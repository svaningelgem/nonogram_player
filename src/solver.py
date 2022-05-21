from typing import List

from .utils import cross
from .exceptions import NoSpaceLeft
from .line import Line
from .solver_common_line_fields import CommonLineFields


def skip_crosses(line: Line, idx: int) -> int:
    try:
        while line[idx] == cross:
            idx += 1
    except IndexError:
        ...

    return idx


class Solver:
    def get_sureties(self, line: Line, nrs: List[int]):
        """Returns which fields are certain to be either filled or a cross."""

        box = CommonLineFields()

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

