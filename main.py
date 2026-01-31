import pandas as pd
import numpy as np


def main(cell_count):
    print(cell_count)


if __name__ == '__main__':
    # read in csv
    cc = pd.read_csv('cell-count.csv')
    main(cc)
    