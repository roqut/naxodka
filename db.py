# db.py
import psycopg2

class Database:
    def __init__(self, dbname, user, password):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host='192.168.8.56',
            port='5432'
        )
        self.cur = self.conn.cursor()

    def fetch_all(self, query, *params):
        self.cur.execute(query, *params)
        return self.cur.fetchall()
    
    def execute(self, query):
        self.cur.execute(query)

    def commit(self):
        self.conn.commit()
        
    def close(self):
        self.conn.close()
