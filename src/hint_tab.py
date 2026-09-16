from dataclasses import dataclass, field

import numpy as np
from PIL.Image import Image


@dataclass
class HintTab:
    direction: str
    img: Image

    shapes: list[tuple[int, int]] = field(default_factory=list)
    nr_imgs: list[list[np.ndarray]] = None

    def __post_init__(self):
        self.arr = np.array(self.img)

    def __len__(self):
        return len(self.shapes)
