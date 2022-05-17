from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import numpy as np
from PIL.Image import Image


@dataclass
class HintTab:
    direction: str
    img: Image

    shapes: List[Tuple[int, int]] = field(default_factory=list)
    nr_imgs: List[List[np.ndarray]] = None

    def __post_init__(self):
        self.arr = np.array(self.img)

    def __len__(self):
        return len(self.shapes)
