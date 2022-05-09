from pathlib import Path
from pprint import pprint


class NumberReader:
    def __init__(self):
        self.nets = sorted((
            (float(file.stem.split('-')[-1]), file)
            for file in (Path(__file__).parent / 'nets').glob('*.hdf5')
        ), key=lambda x: x[0])

        min_ = min(x[0] for x in self.nets)
        total = sum(x[0] for x in self.nets) - len(self.nets) * min_
        total_mins = len(self.nets) - sum(1 for x in self.nets if x[0] == min_)
        lowest_net_counts_for_x_pct = 0.1

        pprint(self.nets)
        # Assign each net its relative % (more reliable nets weigh for more %)
        for i, (acc, file) in enumerate(self.nets):
            if acc == min_:
                pct = lowest_net_counts_for_x_pct
            else:
                acc -= min_
                pct = (acc / total) * (1 - total_mins * lowest_net_counts_for_x_pct)
            self.nets[i] = (pct, file)

        print(sum(x[0] for x in self.nets))


if __name__ == '__main__':
    nr = NumberReader()
    pprint(nr.nets)
    a = 1