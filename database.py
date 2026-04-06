import psycopg2

db = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="root",
    database="auth_system_pg"
)
cursor = db.cursor()