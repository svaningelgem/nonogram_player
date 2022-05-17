import pickle
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List

from skimage.metrics import structural_similarity

from src.utils import all_final_number_files, scale_to_100x100


@dataclass
class Metrics:
    min_: float = 0.0
    max_: float = 0.0
    count: List[float] = field(default_factory=list)

    @property
    def average(self):
        return sum(self.count) / len(self.count)

    def add(self, nr: float):
        if nr <= -100:
            return

        self.min_ = min(self.min_, nr)
        self.max_ = max(self.max_, nr)

        if nr < 1.0:
            self.count.append(nr)


rets: Dict[str, Dict[str, Metrics]] = defaultdict(lambda: defaultdict(Metrics))
scores: Dict[str, Dict[str, Metrics]] = defaultdict(lambda: defaultdict(Metrics))



processed = set()


for first in all_final_number_files:
    first_img = scale_to_100x100(first)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    # detector = cv2.ORB_create()
    detector = cv2.AKAZE_create()

    (target_kp, target_des) = detector.detectAndCompute(first_img, None)

    for second in all_final_number_files:
        to_process = (first, second)
        if to_process in processed:
            continue

        processed.add(to_process)

        second_img = scale_to_100x100(second)

        (comparing_kp, comparing_des) = detector.detectAndCompute(second_img, None)
        if comparing_des is None:
            # print(f"{second}: not the same?")
            if second.parent.name == '2':
                raise ValueError
            continue  # Not the same?

        matches = bf.match(target_des, comparing_des)
        dist = [m.distance for m in matches]
        if not dist:
            ret = -100
        else:
            ret = sum(dist) / len(dist)

        score = structural_similarity(first_img, second_img)
        # print(f'{second}: ret: {ret}, score: {score}')
        rets[first.parent.name][second.parent.name].add(ret)
        scores[first.parent.name][second.parent.name].add(score)


Path('rets.dat').write_bytes(pickle.dumps(dict(rets)))
Path('scores.dat').write_bytes(pickle.dumps(dict(scores)))
