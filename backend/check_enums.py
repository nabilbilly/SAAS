import sqlalchemy as sa
from app.db.session import engine

def ultimate_check():
    try:
        with engine.connect() as conn:
            # 1. Find the exact type OID and details for the status column
            query = sa.text("""
                SELECT 
                    n.nspname AS schema_name,
                    t.typname AS type_name,
                    t.oid AS type_oid,
                    e.enumlabel AS label
                FROM pg_attribute a
                JOIN pg_class c ON a.attrelid = c.oid
                JOIN pg_type t ON a.atttypid = t.oid
                JOIN pg_namespace n ON n.oid = t.typnamespace
                LEFT JOIN pg_enum e ON t.oid = e.enumtypid
                WHERE c.relname = 'admission' 
                AND a.attname = 'status'
                ORDER BY e.enumsortorder
            """)
            results = conn.execute(query).fetchall()
            if not results:
                print("No status column found for 'admission' table.")
                return
                
            first = results[0]
            print(f"COLUMN_TYPE: {first[0]}.{first[1]} (OID: {first[2]})")
            print(f"VALID_LABELS: {[r[3] for r in results if r[3] is not None]}")
            
            # 2. Check data
            query_data = sa.text("SELECT status, count(*) FROM admission GROUP BY status")
            data = conn.execute(query_data).fetchall()
            print(f"STORED_DATA: {data}")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    ultimate_check()
