import sqlalchemy as sa
from app.db.session import engine
import sys

def check_clean():
    with open("enum_check.log", "w") as f:
        try:
            with engine.connect() as conn:
                f.write("\n--- CHECKING PG_ENUM LABELS ---\n")
                query_labels = sa.text("""
                    SELECT e.enumlabel 
                    FROM pg_enum e
                    JOIN pg_type t ON e.enumtypid = t.oid
                    WHERE t.typname = 'admissionstatus'
                    ORDER BY e.enumsortorder;
                """)
                labels = conn.execute(query_labels).fetchall()
                clean_labels = [row[0] for row in labels]
                f.write(f"ENUM LABELS: {clean_labels}\n")

                f.write("\n--- CHECKING RAW SQL INSERTION/SELECTION ---\n")
                # Try to select using 'Rejected'
                try:
                    res = conn.execute(sa.text("SELECT count(*) FROM admission WHERE status = 'Rejected'"))
                    f.write(f"Query with 'Rejected' SUCCEEDED. Count: {res.scalar()}\n")
                except Exception as e:
                    f.write(f"Query with 'Rejected' FAILED: {e}\n")
                    conn.rollback()

                # Try to select using 'REJECTED'
                try:
                    res = conn.execute(sa.text("SELECT count(*) FROM admission WHERE status = 'REJECTED'"))
                    f.write(f"Query with 'REJECTED' SUCCEEDED. Count: {res.scalar()}\n")
                except Exception as e:
                    f.write(f"Query with 'REJECTED' FAILED: {e}\n")
                    conn.rollback()

        except Exception as e:
            f.write(f"CRITICAL FAULT: {e}\n")

if __name__ == "__main__":
    check_clean()
