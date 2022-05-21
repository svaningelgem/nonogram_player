from dataclasses import dataclass

from src.hint_tab import HintTab


@dataclass
class Grid:
    left: HintTab
    top: HintTab
