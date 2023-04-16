from pydantic import BaseModel
import psycopg2

class Database:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()

    def get_contractor_email(self, contractor_id):
        self.connect()
        cur = self.conn.cursor()
        query = f"SELECT \"Name\",\"Email\" FROM \"Contractor\" c WHERE c.\"Id\" = {contractor_id}"
        cur.execute(query)
        name, email = cur.fetchone()
        cur.close()
        self.disconnect()
        return name, email


