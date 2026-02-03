import sys
import os
import sqlite3
from functools import total_ordering

import pandas as pd
import seaborn as sns

import database.initialize_db as init_db
import database.sqlite_connection as db_conn


def main(cell_count):
    
    # Part 1: Data Management
    data_management(cell_count)
    
    # Part 2: Data Overview
    data_overview()
    
    # Part 3: Statistical Analysis
    # statistical_analysis()
    
    print("finished")
    
    
def data_management(cell_count):
    """
    PART 1: DATA MANAGEMENT
    """
    # first check if database exists
    if not os.path.exists("database/teiko_db.db"):
        db_init_success = init_db.create_database(cell_count)
        
        if not db_init_success:
            print("Check database initialization for errors")
            sys.exit(1)
            

def data_overview():
    """
        PART 2: INITIAL ANALYSIS - DATA OVERVIEW
            - create cell type frequency summary table
            - columns needed: sample, total_count, population, count, percentage
        """
    # establish database connection
    db_path = "database/teiko_db.db"
    with db_conn.sqlite_connection(db_path) as connection:
        cursor = connection.cursor()
        try:
            # create total_count column in results table
            cursor.execute("PRAGMA table_info(results);")
            columns = [row[1] for row in cursor.fetchall()]
            
            if "total_count" not in columns:
                cursor.execute("""
                    ALTER TABLE results
                    ADD COLUMN total_count INTEGER;
                """)
                cursor.execute("""
                    UPDATE results
                    SET total_count = b_cell + cd8_t_cell + cd4_t_cell + nk_cell + monocyte
                """)
        except sqlite3.Error as e:
            print("ERROR ADDING total_count COLUMN TO results TABLE")
            print(e)
            
        try:
            # create population_summary table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS population_summary (
                    summary_id INTEGER PRIMARY KEY,
                    sample_id INTEGER NOT NULL,
                    population TEXT NOT NULL,
                    count INTEGER NOT NULL,
                    total_count INTEGER NOT NULL,
                    percentage REAL NOT NULL,
                    FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
                );
            """)
            cursor.execute("""
                INSERT INTO population_summary (sample_id, population, count, total_count, percentage)
                SELECT sample_id, 'b_cell' AS population, b_cell AS count, total_count,
                       CAST(b_cell AS REAL) / total_count AS percentage
                FROM results
                
                UNION ALL
                SELECT sample_id, 'cd8_t_cell', cd8_t_cell, total_count,
                       CAST(cd8_t_cell AS REAL) / total_count
                FROM results
                
                UNION ALL
                SELECT sample_id, 'cd4_t_cell', cd4_t_cell, total_count,
                       CAST(cd4_t_cell AS REAL) / total_count
                FROM results
                
                UNION ALL
                SELECT sample_id, 'nk_cell', nk_cell, total_count,
                       CAST(nk_cell AS REAL) / total_count
                FROM results
                
                UNION ALL
                SELECT sample_id, 'monocyte', monocyte, total_count,
                       CAST(monocyte AS REAL) / total_count
                FROM results;
            """)
        except sqlite3.Error as e:
            print("ERROR CREATING population_summary TABLE")
            print(e)


def statistical_analysis():
    pass
    
    
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
    