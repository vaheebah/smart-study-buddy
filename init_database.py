#!/usr/bin/env python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

print("\n[*] Initializing Database Tables...")

engine = create_engine(os.getenv('DATABASE_URL'))

# Read SQL schema
with open('scripts/init_db.sql', 'r') as f:
    sql_commands = f.read()

# Execute SQL
with engine.connect() as conn:
    conn.execute(text(sql_commands))
    conn.commit()
    print(" Database tables created successfully!")

print("\n[*] Verifying tables...")
with engine.connect() as conn:
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
    tables = result.fetchall()
    for table in tables:
        print(f"   - {table[0]}")

print("\nDatabase initialization complete!\n")

