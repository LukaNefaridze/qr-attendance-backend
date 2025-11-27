# Setting Up This Computer as MySQL Host (Windows)

This guide will help you configure this Windows computer to host MySQL and accept remote connections.

## Prerequisites

- MySQL 8.0 installed and running (MySQL80 service)
- Administrator privileges
- Both computers on the same network

## Quick Setup

### Step 1: Run the Setup Script

1. **Right-click** `setup_mysql_host.bat` and select **"Run as administrator"**
2. The script will:
   - Configure MySQL to accept remote connections
   - Set up Windows Firewall
   - Display your IP address

### Step 2: Create Remote Database User

1. Open Command Prompt or PowerShell
2. Connect to MySQL:
   ```cmd
   mysql -u root -p
   ```
   (Enter your MySQL root password when prompted)

3. Run the user setup script:
   ```sql
   source setup_mysql_remote_user.sql
   ```
   
   Or manually execute:
   ```sql
   CREATE USER 'attendance_user'@'%' IDENTIFIED BY 'attendance_secure_pass_2024!';
   GRANT ALL PRIVILEGES ON attendance_db.* TO 'attendance_user'@'%';
   FLUSH PRIVILEGES;
   ```

### Step 3: Update Django Settings

On **this host computer**, update `attendance_system/settings.py` to use localhost:

The settings should use `127.0.0.1` or leave `DB_HOST` unset (it will default to localhost).

Current default in settings.py uses `192.168.56.1` - we should change this to `127.0.0.1` for the host computer.

### Step 4: Find Your IP Address

After running the setup script, note your **Wi-Fi IP address** (usually `192.168.50.x` or `192.168.1.x`).

You can also check it manually:
```cmd
ipconfig
```
Look for "Wireless LAN adapter Wi-Fi" → IPv4 Address

**Your IP Address:** `192.168.50.108` (from current network configuration)

### Step 5: Test the Setup

Test that MySQL is listening on all interfaces:
```cmd
netstat -an | findstr :3306
```

You should see:
```
TCP    0.0.0.0:3306           0.0.0.0:0              LISTENING
```

## Manual Configuration (If Script Doesn't Work)

### 1. Edit MySQL Configuration

1. Open `C:\ProgramData\MySQL\MySQL Server 8.0\my.ini` in Notepad (as Administrator)
2. Find the `[mysqld]` section
3. Add or modify:
   ```
   bind-address = 0.0.0.0
   ```
4. Save the file
5. Restart MySQL service:
   ```cmd
   net stop MySQL80
   net start MySQL80
   ```

### 2. Configure Windows Firewall

Open PowerShell as Administrator and run:
```powershell
netsh advfirewall firewall add rule name="MySQL" dir=in action=allow protocol=TCP localport=3306
```

### 3. Create Remote User

Connect to MySQL and run:
```sql
CREATE USER 'attendance_user'@'%' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON attendance_db.* TO 'attendance_user'@'%';
FLUSH PRIVILEGES;
```

## Configuration Summary

**Host Computer (This Computer):**
- MySQL Host: `127.0.0.1` (localhost)
- Database: `attendance_db`
- User: `root` (or `attendance_user` if you prefer)
- Password: Your MySQL root password
- IP Address for Remote Access: `192.168.50.108` (your Wi-Fi IP)

**Remote Computer (Other Computer):**
- MySQL Host: `192.168.50.108` (this computer's IP)
- Database: `attendance_db`
- User: `attendance_user`
- Password: `attendance_secure_pass_2024!` (or the password you set)

## Testing Remote Connection

From the remote computer, test the connection:
```cmd
mysql -h 192.168.50.108 -u attendance_user -p attendance_db
```

## Troubleshooting

### MySQL Service Not Running
```cmd
net start MySQL80
```

### Connection Refused
- Check if MySQL is listening: `netstat -an | findstr :3306`
- Verify `bind-address = 0.0.0.0` in my.ini
- Check Windows Firewall rules

### Access Denied
- Verify username and password
- Check user privileges: `SHOW GRANTS FOR 'attendance_user'@'%';`
- Ensure database exists: `SHOW DATABASES;`

### Can't Find Host
- Verify both computers are on the same network
- Ping the host IP: `ping 192.168.50.108`
- Check if IP address changed (consider setting static IP)

## Security Notes

1. **Change the default password** - Use a strong password for `attendance_user`
2. **Restrict IP access** - Instead of `'%'`, use specific IP range like `'192.168.50.%'`
3. **Don't expose to internet** - Only use on local network
4. **Use SSH tunneling** - For better security (advanced)

## Next Steps

1. ✅ Run `setup_mysql_host.bat` as administrator
2. ✅ Create remote user using `setup_mysql_remote_user.sql`
3. ✅ Update Django settings to use `127.0.0.1` on this computer
4. ✅ Share your IP address (`192.168.50.108`) with the remote computer
5. ✅ Configure the remote computer to connect to your IP

Both computers will now share the same database!

