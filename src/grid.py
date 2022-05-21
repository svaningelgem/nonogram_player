from dataclasses import dataclass
from typing import Dict, List

import numpy as np

from src.utils import unknown
from src.exceptions import CannotSolve, FullySolved, NoSimilaritiesFound, NotMatchingChars
from src.hint_tab import HintTab
from src.line import Line
from src.solver_common_line_fields import CommonLineFields
from src.solver_line_possibilties import LinePossibilityGenerator


@dataclass
class Grid:
    left: HintTab
    top: HintTab
