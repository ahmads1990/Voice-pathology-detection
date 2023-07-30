from Database.tables import connection, getCursor, save_close, save, init
from Database.dtos import Patient, Session, Pathology

class DatabaseHandler():
    def __init__(self):
        # Setting cursor
        self.db = connection()
        init(self.db, getCursor(self.db))

    # -----------------------------------------
    # Insert Data In Tables
    # -----------------------------------------

    # patient
    def insert_patient(self, patient):
        db = connection()
        cr = getCursor(db)
        cr.execute(f"""
                    INSERT INTO patients(id, name, age, gender, phone_number, email)
                    VALUES(
                        {patient.id}, 
                        '{patient.name}',
                        {patient.age},
                        '{patient.gender}',
                        '{patient.phone}',
                        '{patient.email}')
                    """)
        save(db)

    # session
    def insert_session(self, session):
        db = connection()
        cr = getCursor(db)
        cr.execute(
        f"""
        INSERT INTO sessions (patient_id, audio_path, pathology_id, doctor_diagnoses, Letters, Phrase)
        VALUES (
            {session.patient_id},
            '{session.audio_path}',
            {session.pathology_id},
            '{session.doctor_diagnoses}',
            {int(session.letters)},
            {int(session.phrase)}
        );
        """)
        save(db)
        
        last_inserted_id = cr.lastrowid  # Retrieve the newly created primary key
        return last_inserted_id

    # pathology
    def insert_pathology(self, id, description, name, type):
        db = connection()
        cr = getCursor(db)
        cr.execute(f"INSERT INTO pathologies VALUES({id}, '{description}', '{name}', '{type}')")
        save(db)

    # -----------------------------------------
    # Select All data
    # -----------------------------------------
    def all_data_patients(self):
        db = connection()
        cr = getCursor(db)
        cr.execute(f"SELECT * FROM patients")
        data = cr.fetchall()
        db.close()
        return data

    def all_data_sessions(self):
        db = connection()
        cr = getCursor(db)
        cr.execute(f"SELECT * FROM sessions")
        data = cr.fetchall()
        db.close()
        return data

    def all_data_pathologies(self):
        db = connection()
        cr = getCursor(db)
        cr.execute(f"SELECT * FROM pathologies")
        data = cr.fetchall()
        db.close()
        return data

    def fetch_pathologies(self):
        # Connect to the SQLite database
        db = connection()

        # Create a cursor object to execute SQL commands
        cursor = getCursor(db)

        # Select all entries from the "pathologies" table
        cursor.execute("SELECT id, name, description FROM pathologies")
        rows = cursor.fetchall()

        # Create a dictionary to store the results
        pathologies_dict = {}

        # Process the rows and populate the dictionary
        for row in rows:
            pathology_id, name, description = row
            pathologies_dict[pathology_id] = [name, description]

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return pathologies_dict


    # -----------------------------------------
    # Select by ID
    # -----------------------------------------

    # patient
    def select_patient_by_id(self, patient_id):
        db = connection()
        cr = getCursor(db)
        # Execute the SELECT query
        cr.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))    

        # Fetch the result
        result = cr.fetchone()
        db.close()
        # Map the result to Patient DTO object
        if result:
            patient = Patient(result[0], result[1], result[5], result[4], result[2], result[3])
            return patient
        else:
            return None
        
    # sessions
    def select_sessions_by_patient_id(self, patient_id):
        db = connection()
        cr = getCursor(db)
        # Execute the SELECT query
        cr.execute("SELECT * FROM sessions WHERE patient_id = ?", (patient_id,))

        # Fetch all the results
        results = cr.fetchall()
        db.close()
        # Map the results to SessionDto objects
        sessions = []
        for result in results:
            session = Session(result[0], result[2], result[3], result[4], result[5], result[6])
            sessions.append(session)

        return sessions
    def select_last_session_id(self):
        db = connection()
        cr = getCursor(db)
        # Execute the query to get the last session ID
        query = "SELECT session_id FROM sessions ORDER BY session_id DESC LIMIT 1;"
        cr.execute(query)
        # Fetch the result
        result = cr.fetchone()
        db.close()
        # Print the last session ID
        if result:
            last_session_id = result[0]
            print("Last Session ID:", last_session_id)
            return last_session_id
        else:
            print("No sessions found")
            return -1
            
    # pathology 
    def get_pathology_by_name(self, name):
        db = connection()
        cr = getCursor(db)
        # Execute the SELECT query
        cr.execute("SELECT * FROM pathologies WHERE name = ?", (name,))
        # Fetch the result
        result = cr.fetchone()
        db.close()
        print(result)
        print(name  )
        # If no result found, return None
        if result is None:
            return None

        # Create a Pathology object from the result
        pathology = Pathology(result[0], result[1], result[2], result[3])

        return pathology
    # -----------------------------------------
    # Delete by ID
    # -----------------------------------------
    def delete_patient(self, id):
        db = connection()
        cr = getCursor(db)
        cr.execute(f"DELETE FROM patients WHERE id={id}")
        save(self.db)

    def delete_session(self, session_id):
        db = connection()
        cr = getCursor(db)
        cr.execute(f"DELETE FROM sessions WHERE session_id={session_id}")
        save(self.db)

    def delete_pathology(self, id):
        db = connection()
        cr = getCursor(db)
        cr.execute(f"DELETE FROM pathologies WHERE id={id}")
        save(self.db)

    # -----------------------------------------
    # Update
    # -----------------------------------------

    def update_session_pathology_id(self,session_id, pathology_id):
        db = connection()
        #cr = getCursor(db)
        # Execute the UPDATE query
        db.execute("UPDATE sessions SET pathology_id = ? WHERE session_id = ?", (pathology_id, session_id))

        # Commit the changes
        db.commit()
        
        db.close()

    def phrases_letters(self, session_id):
        db = connection()
        cr = getCursor(db)
        query = f"UPDATE sessions SET Letters='DONE', Phrase='DONE' WHERE session_id={session_id}"
        cr.execute(query)
        save(self.db)
