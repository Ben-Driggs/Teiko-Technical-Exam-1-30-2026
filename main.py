import sys
import os
import pandas as pd
import numpy as np

import database.initialize_db as init_db


def main(cell_count):
    # first check if database exists
    if not os.path.exists("/database/teiko_db.db"):
        db_init_success = init_db.createDatabase(cell_count)
        
        if not db_init_success:
            print("Check database initialization for errors")
            sys.exit()
            
    print("finished")
    
    
if __name__ == '__main__':
    # read in csv
    cc = pd.read_csv('cell-count.csv')
    main(cc)
    