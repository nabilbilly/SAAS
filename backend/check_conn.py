import psycopg2
from app.core.config import settings

def check_conn():
    print(f"Attempting to connect to: {settings.sqlalchemy_database_uri}")
    try:
        conn = psycopg2.connect(
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT
        )
        print("Connection successful!")
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    check_conn()
