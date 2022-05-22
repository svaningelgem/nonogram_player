import logging
from dataclasses import dataclass
from math import sqrt
from pathlib import Path
from typing import ClassVar, Dict, List, Tuple, Union

import numpy as np
from PIL.Image import Image
from easyocr import Reader

from src.utils import ImageType, save, scale_to_100x100

logger = logging.getLogger(__name__)


def _extract_pure_image(img_path: Union[Path, str, Image, np.ndarray]) -> np.ndarray:
    tmp = scale_to_100x100(img_path).astype("int8")
    tmp[tmp > 0] = 127
    tmp[tmp < 0] = -1
    return tmp


def _calculate_distance(background: np.ndarray, foreground: np.ndarray) -> float:
    back_white_pixels = np.count_nonzero(background == -1)
    fore_white_pixels = np.count_nonzero(foreground == -1)
    same_white_pixels = np.count_nonzero((foreground == -1) & (background == -1))

    f = fore_white_pixels - same_white_pixels
    b = back_white_pixels - same_white_pixels

    return sqrt(f**2 + b**2)


def _add_border(img: np.ndarray, size: int) -> np.ndarray:
    tmp = np.full(
        (img.shape[0] + size * 2, img.shape[1] + size * 2), 255, dtype=img.dtype
    )
    tmp[size: img.shape[0] + size, size: img.shape[1] + size] = img
    return tmp


@dataclass
class InterpretNumber:
    _reference_image_path: ClassVar[Path] = Path(__file__).parent / "reference_images"
    _reference_images: ClassVar[Dict[str, np.ndarray]] = {
        path.stem: _extract_pure_image(path)
        for path in _reference_image_path.glob("*.png")
    }

    image: ImageType
    iteration: int = 0

    def __post_init__(self):
        self.image = _extract_pure_image(self.image)

    def _detect_via_numpy_subtraction(self) -> List[Tuple[str, float]]:
        # Calculate all distances.
        distances = {
            nr: _calculate_distance(self.image, arr)
            for nr, arr in self._reference_images.items()
        }

        # Take the worst as a reference point
        worst = max(distances.values())

        # Convert it into a %
        preds = {nr: 1 - (distance / worst) for nr, distance in distances.items()}

        # Sort them with the first the best
        preds_sorted = sorted(preds.items(), key=lambda x: x[1], reverse=True)

        return preds_sorted

    @property
    def most_likely(self) -> str:
        """
        returns a list of potential numbers. Most likely is first.
        If an OCR detection was waranted, and it didn't find anything >>
            Return a list of the first x (within 5% of the first found number)
        """
        preds = self._detect_via_numpy_subtraction()
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Saving image to: %s', save(self.image, subfolder='debug', increasing=True))
            logger.debug('preds: %s', preds)

        # Too little difference between the first 2. --> I'm not sure this is the right one then!
        if preds[0][1] - preds[1][1] < 0.05:
            ocr_detection = self._detect_via_ocr()
            logger.debug('ocr_detection: %s', ocr_detection)
            if ocr_detection:
                return ocr_detection[0]
            else:
                # Something went wrong in another loop... So we'll need to try something else here!
                return preds[self.iteration][0]

        return preds[0][0]

    # ######################## OCR
    _ocr: ClassVar[Reader] = None

    def _detect_via_ocr(self) -> Tuple[str, float]:
        if InterpretNumber._ocr is None:
            InterpretNumber._ocr = Reader(["en", "nl"])

        args = dict(allowlist=list("0123456789"), detail=1)

        work = self.image.copy().astype("uint8")
        detection = (
            InterpretNumber._ocr.readtext(work, **args)
            # Add border & try again
            or InterpretNumber._ocr.readtext(
                _add_border(work, 10).astype("uint8"), **args
            )
        )
        if detection:
            return detection[0][1:]

        return []


def test_1():
    # some_test = random.sample(all_other_images, 10)
    for img in Path(r"E:\nonogram_player\screenshots\nr").rglob("*.png"):
        assert InterpretNumber(img).most_likely == img.parent.name
