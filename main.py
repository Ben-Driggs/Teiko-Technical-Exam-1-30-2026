import sys
import os
import pandas as pd
import numpy as np

import database.initialize_db as init_db


def main(cell_count):
    # first check if database exists
    if not os.path.exists("database/teiko_db.db"):
        db_init_success = init_db.create_database(cell_count)
        
        if not db_init_success:
            print("Check database initialization for errors")
            sys.exit(1)
            
    print("finished")
    
    
if __name__ == '__main__':
    # read in csv
    try:
        cc = pd.read_csv('cell-count.csv')
    except FileNotFoundError as e:
        print("Couldn't find 'cell-count.csv' file. Make sure this csv is in the main working directory.")
        print(e)
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)
        
    main(cc)
    