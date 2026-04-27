# Supabase Database Setup Guide

Complete guide to set up your free Supabase PostgreSQL database for the AI Content Generator.

## Step 1: Create Supabase Account

1. Go to [https://supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign up with GitHub, Google, or email (100% FREE, no credit card required)

## Step 2: Create New Project

1. After logging in, click "New Project"
2. Fill in the details:
   - **Project Name**: `ai-content-generator` (or your choice)
   - **Database Password**: Create a strong password (SAVE THIS!)
   - **Region**: Choose closest to your location
   - **Pricing Plan**: Free (500 MB storage, unlimited API requests)
3. Click "Create new project"
4. Wait 2-3 minutes for project initialization

## Step 3: Get Database Connection Details

1. In your Supabase project dashboard, click "Settings" (gear icon)
2. Go to "Database" section
3. Scroll down to "Connection string" section
4. Copy the following details:

```
Host: db.<your-project-ref>.supabase.co
Database name: postgres
Port: 5432
User: postgres
Password: <your-database-password>
```

### Connection String Format:
```
postgresql://postgres:<your-password>@db.<your-project-ref>.supabase.co:5432/postgres
```

## Step 4: Run Database Schema

1. In Supabase dashboard, click "SQL Editor" in the left sidebar
2. Click "New query"
3. Copy and paste the entire content from `schema.sql` file
4. Click "Run" button (or press Ctrl+Enter)
5. You should see "Success. No rows returned" message

## Step 5: Verify Tables Created

1. Click "Table Editor" in the left sidebar
2. You should see 3 tables:
   - `users`
   - `chat_sessions`
   - `chat_messages`
3. Click on each table to verify columns are created correctly

## Step 6: Configure Spring Boot Application

1. Open `backend/src/main/resources/application.properties`
2. Update the database configuration:

```properties
spring.datasource.url=jdbc:postgresql://db.<your-project-ref>.supabase.co:5432/postgres
spring.datasource.username=postgres
spring.datasource.password=<your-database-password>
```

### Using Environment Variables (Recommended for Production):

Create a `.env` file in the `backend` directory:

```bash
SUPABASE_HOST=db.<your-project-ref>.supabase.co
SUPABASE_PORT=5432
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=<your-database-password>
JWT_SECRET=your-256-bit-secret-key-change-this-in-production
AI_SERVICE_URL=http://localhost:8000
```

## Step 7: Test Database Connection

### Option 1: Using psql (Command Line)

```bash
psql "postgresql://postgres:<your-password>@db.<your-project-ref>.supabase.co:5432/postgres"
```

### Option 2: Using DBeaver or pgAdmin

1. Download [DBeaver](https://dbeaver.io/) (free) or [pgAdmin](https://www.pgadmin.org/)
2. Create new PostgreSQL connection
3. Enter the connection details from Step 3
4. Test connection

### Option 3: Run Spring Boot Application

```bash
cd backend
./mvnw spring-boot:run
```

If connection is successful, you'll see:
```
HikariPool-1 - Start completed.
```

## Step 8: Enable Row Level Security (Optional but Recommended)

For production, enable RLS to secure your data:

1. In Supabase SQL Editor, run:

```sql
-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

-- Create policies (example for users table)
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);
```

**Note**: Since we're using JWT authentication in Spring Boot (not Supabase Auth), you may skip RLS or configure it based on your security requirements.

## Supabase Free Tier Limits

✅ **Included in Free Tier:**
- 500 MB database storage
- Unlimited API requests
- 50,000 monthly active users
- 2 GB file storage
- 5 GB bandwidth
- 7-day log retention
- Community support

## Troubleshooting

### Connection Timeout
- Check if your IP is allowed (Supabase allows all IPs by default)
- Verify firewall settings
- Try using connection pooler: `db.<project-ref>.supabase.co:6543`

### Authentication Failed
- Double-check your database password
- Reset password in Supabase Settings > Database

### Tables Not Created
- Ensure you ran the complete `schema.sql` file
- Check for SQL errors in the SQL Editor
- Verify you're connected to the correct project

### Spring Boot Connection Error
- Verify PostgreSQL driver is in `pom.xml`
- Check `application.properties` configuration
- Ensure database URL format is correct

## Next Steps

After successful setup:

1. ✅ Database is ready
2. ✅ Tables are created
3. ✅ Spring Boot can connect
4. 🚀 Start building your application!

## Useful Supabase Features

### 1. Table Editor
- View and edit data directly in browser
- Add/remove rows manually
- Export data as CSV

### 2. SQL Editor
- Run custom queries
- Create views and functions
- Database migrations

### 3. Database Backups
- Free tier: Daily backups (7-day retention)
- Restore from Settings > Database > Backups

### 4. API Auto-Generation
- Supabase auto-generates REST API for your tables
- Access via: `https://<project-ref>.supabase.co/rest/v1/`
- (We're using Spring Boot API instead, but this is available)

## Support

- **Supabase Docs**: https://supabase.com/docs
- **Community**: https://github.com/supabase/supabase/discussions
- **Discord**: https://discord.supabase.com

---

**Your database is now ready! 🎉**

Proceed to run the Spring Boot backend and Python AI service.
