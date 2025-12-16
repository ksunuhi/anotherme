"""
Migration script to verify existing users
Run this to mark all users created before email verification feature as verified
"""
import sqlite3
from datetime import datetime

# Database path
DB_PATH = "database/anotherme.db"

def migrate_verify_existing_users():
    """Mark all existing users (before 2025-12-12) as email verified"""

    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Update all users created before email verification feature was added
        cutoff_date = '2025-12-12 00:00:00'

        cursor.execute("""
            UPDATE users
            SET email_verified = 1
            WHERE created_at < ?
              AND email_verified = 0
        """, (cutoff_date,))

        updated_count = cursor.rowcount

        # Commit changes
        conn.commit()

        # Show updated users
        cursor.execute("""
            SELECT id, email, full_name, email_verified, created_at
            FROM users
            WHERE email_verified = 1
            ORDER BY created_at
        """)

        users = cursor.fetchall()

        print(f"\n✅ Migration completed successfully!")
        print(f"📊 {updated_count} user(s) marked as verified\n")

        if users:
            print("Verified users:")
            print("-" * 80)
            for user in users:
                user_id, email, full_name, verified, created_at = user
                print(f"  • {full_name} ({email})")
                print(f"    Created: {created_at}")
            print("-" * 80)

        # Close connection
        conn.close()

        print(f"\n✅ All existing users can now log in!")

    except Exception as e:
        print(f"❌ Error during migration: {e}")
        raise

if __name__ == "__main__":
    print("🔧 Running migration: Verify existing users")
    print("=" * 80)
    migrate_verify_existing_users()
