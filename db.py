import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        dbname="phiogre_db",
        user="phiogre_user",
        password=os.environ.get("DB_PASSWORD"),
        host="dpg-d0sbsg7fte5s73dmlo30-a",
        port="5432"
    )
