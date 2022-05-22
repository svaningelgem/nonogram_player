from itertools import count
from typing import List

import numpy as np
from multipledispatch import dispatch

from src.exceptions import NotMatchingChars
from src.utils import cross, unknown


class Line:
    @dispatch(int)
    def __init__(self, len_: int):
        self._inner = [unknown] * len_

    @dispatch(list)
    def __init__(self, fields: List[int]):  # noqa: F811
        self._inner = fields.copy()

    @dispatch(np.ndarray)
    def __init__(self, fields: np.ndarray):  # noqa: F811
        self._inner = list(fields)

    def __len__(self):
        return len(self._inner)

    @staticmethod
    def ltrim(line) -> "Line":
        line = line.copy()

        # ltrim the list
        while line and line[0] == cross:
            line = line[1:]

        return line

    @staticmethod
    def rtrim(line) -> "Line":
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
        return str(["x" if x is cross else x for x in self._inner])

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self._inner == other._inner

    def __getitem__(self, index: int) -> int:
        return self._inner[index]

    def __setitem__(self, index: int, value: int) -> None:
        if index >= len(self._inner):
            raise IndexError

        self._inner[index] = value

    def fill_unknown_with_cross(self) -> "Line":
        return Line([x if x != unknown else cross for x in self._inner])

    def can_merge(self, other: "Line") -> bool:
        assert isinstance(other, Line), f'other is type {type(other)}. Should be "Line"!'
        assert len(other) == len(self._inner)

        for idx, mine, incoming in zip(count(), self._inner, other):
            if mine == unknown or incoming == unknown:
                continue

            # here both are known
            if mine != incoming:  # but not the same? >> Can't merge!
                raise NotMatchingChars(
                    f"Position {idx}: confirmed: {mine}, incoming: {incoming}"
                )

        return True

    def merge(self, other: "Line"):
        self.can_merge(other)

        for idx, (mine, incoming) in enumerate(zip(self._inner, other)):
            if mine == unknown:
                self._inner[idx] = incoming
