from dataclasses import dataclass
from itertools import count

from src.exceptions import NoSimilaritiesFound
from src.line import Line
from src.utils import unknown


@dataclass
class CommonLineFields:
    line: Line = None

    def intersect(self, other: Line):
        assert isinstance(other, Line)

        if self.line is None:
            self.line = other
            return

        assert len(other) == len(self.line)

        for idx, mine, incoming in zip(count(), self.line, other):
            if mine == unknown:
                continue

            if mine != incoming:
                self.line[idx] = unknown

        if all(x == unknown for x in self.line):
            raise NoSimilaritiesFound
