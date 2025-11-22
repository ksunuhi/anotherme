"""
Initialize the database
Run this script to create the database using the SQL schema
"""
import subprocess
import os
from pathlib import Path

def init_database():
    """Initialize SQLite database using schema.sql"""

    # Get paths
    backend_dir = Path(__file__).parent
    db_path = backend_dir / "database" / "anotherme.db"
    schema_path = backend_dir / "database" / "schema.sql"

    # Check if schema file exists
    if not schema_path.exists():
        print(f"❌ Error: Schema file not found at {schema_path}")
        return False

    # Create database directory if it doesn't exist
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Remove old database if exists
    if db_path.exists():
        response = input(f"⚠️  Database already exists at {db_path}. Delete and recreate? (y/N): ")
        if response.lower() != 'y':
            print("❌ Cancelled.")
            return False
        db_path.unlink()
        print("🗑️  Old database deleted.")

    # Create database using schema.sql
    try:
        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        # Run sqlite3 command
        result = subprocess.run(
            ['sqlite3', str(db_path)],
            input=schema_sql,
            text=True,
            capture_output=True
        )

        if result.returncode != 0:
            print(f"❌ Error creating database: {result.stderr}")
            return False

        print(f"✅ Database created successfully at {db_path}")

        # Verify tables were created
        result = subprocess.run(
            ['sqlite3', str(db_path), '.tables'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            tables = result.stdout.strip()
            print(f"✅ Tables created: {tables}")

        return True

    except FileNotFoundError:
        print("❌ Error: sqlite3 command not found. Please install SQLite3.")
        print("\nAlternative: Run this command manually:")
        print(f"   sqlite3 {db_path} < {schema_path}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("AnotherMe - Database Initialization")
    print("=" * 60)
    print()

    success = init_database()

    print()
    print("=" * 60)
    if success:
        print("✅ Database initialization complete!")
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Create .env file: cp .env.example .env")
        print("3. Run the server: uvicorn main:app --reload")
    else:
        print("❌ Database initialization failed.")
        print()
        print("Manual steps:")
        print("1. cd backend")
        print("2. sqlite3 database/anotherme.db < database/schema.sql")
    print("=" * 60)
