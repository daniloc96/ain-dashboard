
import asyncio
import os
import sys

# Debug paths
print(f"CWD: {os.getcwd()}")
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")
sys.path.insert(0, '/app')

try:
    from database.manager import DatabaseManager
except ImportError as e:
    print(f"ImportError: {e}")
    print(f"Sys Path: {sys.path}")
    if os.path.exists('/app'):
        print(f"App dir content: {os.listdir('/app')}")
    if os.path.exists('/app/database'):
        print(f"Database dir content: {os.listdir('/app/database')}")
    raise

from sqlalchemy import text

# Database configuration
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "thewebseller_analytics")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async def add_constraint():
    print(f"Connecting to {DATABASE_URL}...")
    db = DatabaseManager(DATABASE_URL)
    await db.initialize()
    
    try:
        async with db.session() as session:
            # Check if constraint exists
            print("Checking for duplicates...")
            # First clean up duplicates if any (keep latest)
            # This is a bit complex in SQL, but for now let's assumes user handles it or we risk error
            # Actually, to be safe, let's just try to add the constraint. 
            # If it fails due to duplicates, we'll know.
            
            print("Adding unique constraint uq_product_session_ean...")
            await session.execute(text("""
                ALTER TABLE products 
                ADD CONSTRAINT uq_product_session_ean UNIQUE (session, ean);
            """))
            await session.commit()
            print("Constraint added successfully.")
            
    except Exception as e:
        print(f"Error: {e}")
        # If error corresponds to "already exists", specifically ignore
        if "already exists" in str(e):
            print("Constraint already exists.")
        elif "could not create unique index" in str(e):
             print("Duplicates found. Please clean up duplicates manually or dropping table.")
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(add_constraint())
