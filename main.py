import sys
import os
import pandas as pd

import database.initialize_db as init_db


def main(cell_count):
    cell_populations = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]
    
    """
    PART 1: DATA MANAGEMENT
    """
    # first check if database exists
    if not os.path.exists("database/teiko_db.db"):
        db_init_success = init_db.create_database(cell_count)
        
        if not db_init_success:
            print("Check database initialization for errors")
            sys.exit(1)
            
    """
    PART 2: INITIAL ANALYSIS - DATA OVERVIEW
        - create cell type frequency summary table
        - columns needed: sample, total_count, population, count, percentage
    """
    # add total cell count column
    cc['total_count'] = cc[cell_populations].sum(axis=1)
    
    # create summary table
    population_summary = cc.melt(
        id_vars=["sample", "total_count"],
        value_vars=cell_populations,
        var_name="population",
        ignore_index=False,
        value_name="count"
    )
    
    # sort rows by sample
    population_summary = population_summary.sort_values(by=["sample", "population"])
    
    # add percentage column
    population_summary["percentage"] = population_summary["count"] / population_summary['total_count']
    
    # reorder columns
    population_summary = population_summary[["sample", "population", "percentage", "count", "total_count"]]
    
    # save summary table to csv
    try:
        if not os.path.exists("population_summary.csv"):
            population_summary.to_csv("population_summary.csv")
    except Exception as e:
        print(e)
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
    