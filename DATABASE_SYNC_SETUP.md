# Database Synchronization Setup Guide

This guide will help you set up both computers to use the same MySQL database, so changes made on one computer are reflected on the other.

## Overview

You have two options:
1. **Host Computer Setup** (Recommended): One computer hosts MySQL, the other connects to it remotely
2. **Cloud Database**: Use a cloud MySQL service (like AWS RDS, Google Cloud SQL, etc.)

We'll use Option 1 - Host Computer Setup.

## Step 1: Choose the Host Computer

Decide which computer will host the MySQL database. This computer should:
- Be turned on when you want to work
- Have MySQL installed and running
- Be on the same network as the other computer

## Step 2: Configure MySQL on Host Computer

### 2.1 Enable Remote Connections

On the **host computer**, edit MySQL configuration to allow remote connections:

1. Edit MySQL configuration file:
   ```bash
   sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
   ```
   (On some systems it might be `/etc/mysql/my.cnf` or `/etc/my.cnf`)

2. Find the line `bind-address = 127.0.0.1` and change it to:
   ```
   bind-address = 0.0.0.0
   ```
   This allows MySQL to accept connections from any IP address.

3. Restart MySQL:
   ```bash
   sudo systemctl restart mysql
   ```
   or
   ```bash
   sudo service mysql restart
   ```

### 2.2 Create Remote User (Recommended for Security)

It's better to create a dedicated user for remote access instead of using root:

```sql
-- Connect to MySQL
mysql -u root -p

-- Create a user for remote access
CREATE USER 'attendance_user'@'%' IDENTIFIED BY 'your_secure_password';

-- Grant all privileges on attendance_db
GRANT ALL PRIVILEGES ON attendance_db.* TO 'attendance_user'@'%';

-- If you want to allow from specific IP only (more secure):
-- CREATE USER 'attendance_user'@'192.168.1.%' IDENTIFIED BY 'your_secure_password';
-- GRANT ALL PRIVILEGES ON attendance_db.* TO 'attendance_user'@'192.168.1.%';

-- Apply changes
FLUSH PRIVILEGES;
EXIT;
```

### 2.3 Configure Firewall

Allow MySQL port (3306) through the firewall:

**On Ubuntu/Debian:**
```bash
sudo ufw allow 3306/tcp
```

**On CentOS/RHEL:**
```bash
sudo firewall-cmd --permanent --add-port=3306/tcp
sudo firewall-cmd --reload
```

### 2.4 Find Host Computer's IP Address

On the **host computer**, find its IP address:

```bash
# Linux/Mac
ip addr show
# or
ifconfig

# Windows
ipconfig
```

Look for the IP address (usually something like `192.168.1.100` or `10.0.0.5`).

**Note:** If using a dynamic IP, consider setting a static IP or using the computer's hostname.

## Step 3: Configure Django Settings

### 3.1 On Host Computer (where MySQL runs)

Keep the default settings or set environment variables:

```bash
# Optional: Set in your shell or .bashrc
export DB_HOST=127.0.0.1
export DB_NAME=attendance_db
export DB_USER=root
export DB_PASSWORD=1
export DB_PORT=3306
```

Or just use the defaults in `settings.py` (which use `127.0.0.1`).

### 3.2 On Remote Computer (connects to host)

Set environment variables to point to the host computer:

```bash
# Replace <HOST_IP> with the actual IP address from Step 2.4
export DB_HOST=<HOST_IP>
export DB_NAME=attendance_db
export DB_USER=attendance_user  # or 'root' if you didn't create a new user
export DB_PASSWORD=your_secure_password
export DB_PORT=3306
```

**To make this permanent**, add these lines to your `~/.bashrc` or `~/.profile`:

```bash
echo 'export DB_HOST=<HOST_IP>' >> ~/.bashrc
echo 'export DB_NAME=attendance_db' >> ~/.bashrc
echo 'export DB_USER=attendance_user' >> ~/.bashrc
echo 'export DB_PASSWORD=your_secure_password' >> ~/.bashrc
echo 'export DB_PORT=3306' >> ~/.bashrc
source ~/.bashrc
```

## Step 4: Test Connection

### On Remote Computer:

Test the connection:

```bash
# Test MySQL connection
mysql -h <HOST_IP> -u attendance_user -p attendance_db

# Test Django connection
cd /path/to/qr-attendance-backend
source venv/bin/activate
python manage.py check --database default
```

If both work, you're all set!

## Step 5: Run Migrations

**Important:** Only run migrations on ONE computer (preferably the host):

```bash
python manage.py migrate
```

Both computers will now see the same data!

## Troubleshooting

### Connection Refused
- Check if MySQL is running on host: `sudo systemctl status mysql`
- Verify firewall allows port 3306
- Check `bind-address` in MySQL config

### Access Denied
- Verify username and password
- Check user privileges: `SHOW GRANTS FOR 'attendance_user'@'%';`
- Ensure user can connect from remote IP

### Can't Find Host
- Verify both computers are on the same network
- Ping the host IP: `ping <HOST_IP>`
- Check if IP address changed (use static IP if needed)

### Connection Timeout
- Check firewall settings
- Verify MySQL is listening on all interfaces: `netstat -tlnp | grep 3306`

## Security Notes

1. **Use a strong password** for the database user
2. **Consider restricting access** to specific IPs instead of `%` (all IPs)
3. **Use SSH tunneling** for better security (advanced)
4. **Don't expose MySQL to the internet** - only use on local network

## Alternative: Using .env File

Instead of environment variables, you can use a `.env` file with `python-decouple` or `django-environ`:

1. Install: `pip install python-decouple`
2. Create `.env` file:
   ```
   DB_HOST=192.168.1.100
   DB_NAME=attendance_db
   DB_USER=attendance_user
   DB_PASSWORD=your_password
   DB_PORT=3306
   ```
3. Update `settings.py` to use `decouple.config()`

## Quick Reference

**Host Computer:**
- MySQL runs locally
- `DB_HOST=127.0.0.1` or leave unset
- Django connects to local MySQL

**Remote Computer:**
- MySQL runs on host computer
- `DB_HOST=<host_computer_ip>`
- Django connects to remote MySQL

Both computers will see the same database and changes will sync automatically!

