# Database Setup Instructions

## Initialize the Database

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create the database using the schema file:
   ```bash
   sqlite3 database/anotherme.db < database/schema.sql
   ```

3. Verify the tables were created:
   ```bash
   sqlite3 database/anotherme.db
   ```

   Then in SQLite prompt:
   ```sql
   .tables
   .schema users
   .quit
   ```

## Database Schema Overview

### Tables Created:

1. **users** - User accounts and profiles
2. **posts** - User posts/updates
3. **comments** - Comments on posts (supports 1-level nesting)
4. **messages** - Direct messages between users
5. **friendships** - One-way friendship relationships
6. **groups** - Birthday-based and custom groups
7. **group_memberships** - User membership in groups
8. **post_likes** - Track who liked which post
9. **comment_likes** - Track who liked which comment

### Features:

- ✅ Foreign key constraints enabled
- ✅ Indexes on frequently queried columns
- ✅ Automatic triggers for:
  - Like counts (posts & comments)
  - Comment counts (posts)
  - Member counts (groups)
  - Updated timestamps
- ✅ Data validation with CHECK constraints
- ✅ Cascade deletes for referential integrity

## Migration (Future)

For production, we'll use Alembic for database migrations:
```bash
alembic init migrations
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

## Backup Database

```bash
sqlite3 database/anotherme.db ".backup backup.db"
```

## Reset Database

```bash
rm database/anotherme.db
sqlite3 database/anotherme.db < database/schema.sql
```
