import sqlite3


def createDatabase(cell_count):
    connection = sqlite3.connect('C:\\Users\\benny\\PycharmProjects\\Teiko-Technical-Exam-1-30-2026\\database\\teiko_db.db')
    messenger = connection.cursor()
    
    success = True
    
    try:
        messenger.execute("""
            PRAGMA foreign_keys = ON;
        """)
        
        messenger.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                project_id  INTEGER PRIMARY KEY,
                project_name TEXT NOT NULL
            );""")
        
        messenger.execute(
            """
            CREATE TABLE IF NOT EXISTS subjects (
                subject_id INTEGER PRIMARY KEY,
                project_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                condition TEXT NOT NULL,
                age INTEGER NOT NULL,
                sex TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(project_id)
            );""")
            
        messenger.execute("""
            CREATE TABLE IF NOT EXISTS treatments (
                treatment_id INTEGER PRIMARY KEY,
                subject_ID INTEGER NOT NULL,
                treatment TEXT NOT NULL,
                response TEXT,
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
            );""")
            
        messenger.execute("""
            CREATE TABLE IF NOT EXISTS samples (
                sample_id INTEGER PRIMARY KEY,
                subject_id INTEGER NOT NULL,
                treatment_id INTEGER NOT NULL,
                time_from_treatment_start INTEGER NOT NULL,
                sample TEXT NOT NULL,
                sample_type TEXT NOT NULL,
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
                FOREIGN KEY (treatment_id) REFERENCES treatments(treatment_id)
            );""")
            
        messenger.execute("""
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
        
        messenger.executescript("""
            INSERT INTO projects (project_name)
            SELECT DISTINCT project
            FROM raw_data;
            
            INSERT INTO subjects (project_id, subject, condition, age, sex)
            SELECT projects.project_id, subject, condition, age, sex
            FROM raw_data r
            JOIN projects ON projects.project_name = r.project
            GROUP BY projects.project_id, r.subject;
            
            INSERT INTO treatments (subject_id, treatment, response)
            SELECT subjects.subject_id, treatment, response
            FROM raw_data r
            JOIN subjects ON subjects.subject = r.subject;
            
            INSERT INTO samples (subject_id, treatment_id, sample, sample_type, time_from_treatment_start)
            SELECT subjects.subject_id, treatments.treatment_id, sample, sample_type, time_from_treatment_start
            FROM raw_data r
            JOIN subjects ON subjects.subject = r.subject
            JOIN treatments on treatments.subject_id = subjects.subject_id AND treatments.treatment = r.treatment;
            
            INSERT INTO results (sample_id, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte)
            SELECT samples.sample_id, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte
            FROM raw_data r
            JOIN samples ON samples.sample = r.sample;
            
            DROP TABLE raw_data
        """)
        
        connection.commit()
        connection.close()
        
    except sqlite3.OperationalError as e:
        print("ERROR INITIALIZING DATABASE")
        print(e)
        success = False
    finally:
        return success
