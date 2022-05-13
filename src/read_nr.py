from pathlib import Path
from pprint import pprint

import keras
import numpy as np
from PIL import Image


class NumberReader:
    # Retrieved by: {v: int(k) for k, v in train_data.class_indices.items()}
    indices = {
        # index in the network => representing this number in reality
        0: 1,
        1: 10,
        2: 11,
        3: 12,
        4: 13,
        5: 14,
        6: 15,
        7: 2,
        8: 3,
        9: 4,
        10: 5,
        11: 6,
        12: 7,
        13: 8,
        14: 9,
    }

    def __init__(self):
        self._load_net_percentages()
        self._load_models()

    def _load_net_percentages(self):
        self.nets = sorted((
            [float(file.stem.split('-')[-1]), file]
            for file in (Path(__file__).parent / 'nets').glob('*.hdf5')
        ), key=lambda x: x[0])

        min_ = min(x[0] for x in self.nets)
        total = sum(x[0] - min_ for x in self.nets if x[0] != min_)
        total_mins = sum(1 for x in self.nets if x[0] == min_)
        lowest_net_counts_for_x_pct = 0.1
        if len(self.nets) == 1:
            lowest_net_counts_for_x_pct = 1.0
        factor = 1 - total_mins * lowest_net_counts_for_x_pct

        # Assign each net its relative % (more reliable nets weigh for more %)
        for i, (acc, file) in enumerate(self.nets):
            if acc == min_:
                pct = lowest_net_counts_for_x_pct
            else:
                pct = ((acc - min_) / total) * factor
            self.nets[i] = [pct, file]

    def _load_models(self):
        for i, (_, net) in enumerate(self.nets):
            self.nets[i][1] = keras.models.load_model(net)

    def predict(self, nr: np.ndarray) -> int:
        img: Image.Image = Image.fromarray(nr).convert('RGB')

        background = Image.new('RGB', size=(100, 100), color='white')
        background.paste(img, box=(
            (100-img.width)//2,
            (100-img.height)//2,
        ))

        arr = np.reshape(np.array(background), (1, 100, 100, 3))

        totals = np.zeros(len(self.indices))
        for pct, net in self.nets:
            x = net.predict(arr)
            totals += x[0] * pct

        return self.indices[np.argmax(totals)]


if __name__ == '__main__':
    nr = NumberReader()
    a = 1