import os
import sqlite3


def create_database(cell_count):
    db_path = os.path.join(os.path.dirname(__file__), "teiko_db.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    success = True
    
    try:
        cursor.execute("""
            PRAGMA foreign_keys = ON;
        """)
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                project_id  INTEGER PRIMARY KEY,
                project_name TEXT NOT NULL
            );""")
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS subjects (
                subject_id INTEGER PRIMARY KEY,
                project_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                condition TEXT NOT NULL,
                age INTEGER NOT NULL,
                sex TEXT NOT NULL,
                treatment TEXT NOT NULL,
                response TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(project_id)
            );""")
            
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS samples (
                sample_id INTEGER PRIMARY KEY,
                subject_id INTEGER NOT NULL,
                time_from_treatment_start INTEGER NOT NULL,
                sample TEXT NOT NULL,
                sample_type TEXT NOT NULL,
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
            );""")
            
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                result_id INTEGER PRIMARY KEY,
                sample_id INTEGER NOT NULL,
                b_cell INTEGER NOT NULL,
                cd8_t_cell INTEGER NOT NULL,
                cd4_t_cell INTEGER NOT NULL,
                nk_cell INTEGER NOT NULL,
                monocyte INTEGER NOT NULL,
                FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
            );""")
        
        # add raw data table
        cell_count.to_sql("raw_data", connection, if_exists="replace", index=False)
        
        cursor.executescript("""
            INSERT INTO projects (project_name)
            SELECT DISTINCT project
            FROM raw_data;
            
            INSERT INTO subjects (project_id, subject, condition, age, sex, treatment, response)
            SELECT projects.project_id, subject, condition, age, sex, treatment, response
            FROM raw_data r
            JOIN projects ON projects.project_name = r.project
            GROUP BY projects.project_id, r.subject;
            
            INSERT INTO samples (subject_id, sample, sample_type, time_from_treatment_start)
            SELECT subjects.subject_id, sample, sample_type, time_from_treatment_start
            FROM raw_data r
            JOIN subjects ON subjects.subject = r.subject;
            
            INSERT INTO results (sample_id, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte)
            SELECT samples.sample_id, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte
            FROM raw_data r
            JOIN samples ON samples.sample = r.sample;
            
            DROP TABLE raw_data
        """)
        
    except sqlite3.OperationalError as e:
        print("ERROR INITIALIZING DATABASE")
        print(e)
        success = False
    except sqlite3.Error as e:
        print("SQLITE ERROR OCCURRED")
        print(e)
        success = False
    except Exception as e:
        print(e)
        success = False
    finally:
        connection.commit()
        connection.close()
        return success
