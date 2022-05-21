# tests for LinePossibilityGenerator
import unittest

from src.utils import cross, filled
from src.line import Line
from src.solver_line_possibilties import LinePossibilityGenerator

dummy_testcase = unittest.TestCase()
dummy_testcase.maxDiff = None


def test_one_field():
    lpg = LinePossibilityGenerator(5, [1, 1])
    actual = list(lpg)
    expected = [
        Line([filled, cross, filled, cross, cross]),
        Line([filled, cross, cross, filled, cross]),
        Line([filled, cross, cross, cross, filled]),

        Line([cross, filled, cross, filled, cross]),
        Line([cross, filled, cross, cross, filled]),

        Line([cross, cross, filled, cross, filled]),
    ]

    dummy_testcase.assertCountEqual(actual, expected)
