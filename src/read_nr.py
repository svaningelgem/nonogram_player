from pathlib import Path
from pprint import pprint

import keras
import numpy as np
from PIL import Image


class NumberReader:
    # Retrieved from `train_data.class_indices`
    indices = {'1': 0,
               '10': 1,
               '11': 2,
               '12': 3,
               '13': 4,
               '14': 5,
               '15': 6,
               '2': 7,
               '3': 8,
               '4': 9,
               '5': 10,
               '6': 11,
               '7': 12,
               '8': 13,
               '9': 14}
    indices = {v: int(k) for k, v in indices.items()}

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