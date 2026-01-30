import psycopg2
from app.db.session import engine

def fix_enum():
    try:
        # Get URL from engine
        url = engine.url
        dsn = f"postgresql://{url.username}:{url.password}@{url.host}:{url.port}/{url.database}"
        
        # Connect directly with psycopg2
        conn = psycopg2.connect(dsn)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        print("Checking existing labels...")
        cur.execute("SELECT enumlabel FROM pg_enum JOIN pg_type ON pg_enum.enumtypid = pg_type.oid WHERE pg_type.typname = 'admissionstatus'")
        labels = [row[0] for row in cur.fetchall()]
        print(f"Current labels: {labels}")
        
        if 'REJECTED' not in labels:
            print("Adding 'REJECTED' to admissionstatus...")
            cur.execute("ALTER TYPE admissionstatus ADD VALUE 'REJECTED'")
            print("Done.")
        else:
            print("'REJECTED' already exists.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_enum()
