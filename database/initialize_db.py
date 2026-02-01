import sqlite3


def createDatabase():
    connection = sqlite3.connect('C:\\Users\\benny\\PycharmProjects\\Teiko-Technical-Exam-1-30-2026\\database\\teiko_db.db')
    messenger = connection.cursor()
    
    messenger.execute("""
        PRAGMA foreign_keys = ON;
    """)
    
    messenger.execute(
        """
        CREATE TABLE projects (
            project_id  INTEGER PRIMARY KEY,
            project_name TEXT NOT NULL
        );""")
    
    messenger.execute(
        """
        CREATE TABLE subjects (
            subject_id INTEGER PRIMARY KEY,
            project_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            condition TEXT NOT NULL,
            age INTEGER NOT NULL,
            sex TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects(project_id)
        );""")
        
    messenger.execute("""
        CREATE TABLE treatment (
            treatment_id INTEGER PRIMARY KEY,
            subject_ID INTEGER NOT NULL,
            treatment TEXT NOT NULL,
            response TEXT,
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        );""")
        
    messenger.execute("""
        CREATE TABLE samples (
            sample_id INTEGER PRIMARY KEY,
            subject_id INTEGER NOT NULL,
            treatment_id INTEGER NOT NULL,
            sample TEXT NOT NULL,
            sample_type TEXT NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
            FOREIGN KEY (treatment_id) REFERENCES treatments(treatment_id)
        );""")
        
    messenger.execute("""
        CREATE TABLE results (
            result_id INTEGER PRIMARY KEY,
            sample_id INTEGER NOT NULL,
            time_from_treatment INTEGER NOT NULL,
            b_cell INTEGER NOT NULL,
            cd8_t_cell INTEGER NOT NULL,
            cd4_t_cell INTEGER NOT NULL,
            nk_cell INTEGER NOT NULL,
            monocyte INTEGER NOT NULL,
            FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
        );""")
    
    connection.commit()
    connection.close()
