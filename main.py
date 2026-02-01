import os
import pandas as pd
import numpy as np

import database.initialize_db as init_db


def main(cell_count):
    # first check if database exists
    if not os.path.exists("/database/teiko_db.db"):
        init_db.createDatabase()
        
    
if __name__ == '__main__':
    # read in csv
    cc = pd.read_csv('cell-count.csv')
    main(cc)
    