-- MySQL Remote User Setup Script
-- Run this script after configuring MySQL for remote access
-- Execute: mysql -u root -p < setup_mysql_remote_user.sql
-- Or connect to MySQL and paste these commands

-- Create a dedicated user for remote database access
-- Replace 'your_secure_password' with a strong password
CREATE USER IF NOT EXISTS 'attendance_user'@'%' IDENTIFIED BY 'attendance_secure_pass_2024!';

-- Grant all privileges on attendance_db database
GRANT ALL PRIVILEGES ON attendance_db.* TO 'attendance_user'@'%';

-- If you want to restrict access to specific IP range (more secure):
-- Uncomment and modify the following lines:
-- DROP USER IF EXISTS 'attendance_user'@'%';
-- CREATE USER 'attendance_user'@'192.168.50.%' IDENTIFIED BY 'attendance_secure_pass_2024!';
-- GRANT ALL PRIVILEGES ON attendance_db.* TO 'attendance_user'@'192.168.50.%';

-- Apply the changes
FLUSH PRIVILEGES;

-- Verify the user was created
SELECT User, Host FROM mysql.user WHERE User = 'attendance_user';

-- Show grants for the new user
SHOW GRANTS FOR 'attendance_user'@'%';

-- Display success message
SELECT 'Remote user setup complete!' AS Status;
SELECT 'Username: attendance_user' AS Info;
SELECT 'Password: attendance_secure_pass_2024!' AS Info;
SELECT 'IMPORTANT: Change the password to something more secure!' AS Warning;

