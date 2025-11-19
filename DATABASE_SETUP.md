# Database Setup Instructions

## Prerequisites
1. MySQL server must be installed and running
2. Python 3.x installed
3. Django and required packages installed

## Step 1: Create MySQL Database

You have two options:

### Option A: Using MySQL Command Line
```bash
mysql -u root -p < setup_database.sql
```

Or manually:
```sql
CREATE DATABASE IF NOT EXISTS attendance_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Option B: Using MySQL Workbench or phpMyAdmin
1. Open MySQL Workbench or phpMyAdmin
2. Create a new database named `attendance_db`
3. Set character set to `utf8mb4` and collation to `utf8mb4_unicode_ci`

## Step 2: Verify Database Configuration

Check `attendance_system/settings.py` to ensure database credentials match your MySQL setup:
- Database: `attendance_db`
- User: `root`
- Password: `admin123` (change if different)
- Host: `127.0.0.1`
- Port: `3306`

## Step 3: Install Required Packages

If you haven't already, install the MySQL client for Python:
```bash
pip install mysqlclient
```

Or if that fails, try:
```bash
pip install pymysql
```
(If using pymysql, you'll need to add it to your Django settings - see below)

## Step 4: Create Migrations

Run the following command in your project root:
```bash
python manage.py makemigrations
```

Or if using PyCharm:
- Right-click on the project
- Select "Run manage.py Task"
- Enter: `makemigrations`

## Step 5: Apply Migrations

Run migrations to create all database tables:
```bash
python manage.py migrate
```

## Step 6: Create Superuser (Optional)

Create an admin user to access Django admin panel:
```bash
python manage.py createsuperuser
```

## Database Structure

The following models have been created:

1. **User** - Custom user model (extends AbstractUser)
   - Fields: username, email, is_student, is_professor, etc.

2. **Course** - Course information
   - Fields: name, code, professor, created_at, updated_at

3. **Enrollment** - Student enrollment in courses
   - Fields: student, course, enrolled_at
   - Unique constraint: (student, course)

4. **Timetable** - Course schedule
   - Fields: course, day_of_week, start_time, end_time, room

5. **Session** - QR session for attendance
   - Fields: timetable, qr_code, qr_secret, started_at, is_active, expires_at

6. **Attendance** - Student attendance records
   - Fields: student, session, scanned_at, ip_address
   - Unique constraint: (student, session)

## Troubleshooting

### If mysqlclient installation fails:
1. Install MySQL development libraries on your system
2. Or use pymysql as an alternative:
   - Add to `settings.py`:
   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

### If connection errors occur:
- Verify MySQL server is running
- Check database credentials in settings.py
- Ensure database `attendance_db` exists
- Check firewall settings

### If migration errors occur:
- Make sure all previous migrations are applied
- Check for any model conflicts
- Review migration files in `core/migrations/`

