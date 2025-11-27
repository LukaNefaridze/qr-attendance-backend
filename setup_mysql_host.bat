@echo off
REM MySQL Host Setup Script for Windows
REM This script configures MySQL to accept remote connections

echo ========================================
echo MySQL Host Setup Script
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo [1/5] Checking MySQL service status...
sc query MySQL80 | findstr "RUNNING" >nul
if %errorLevel% neq 0 (
    echo ERROR: MySQL80 service is not running!
    echo Please start MySQL service first.
    pause
    exit /b 1
)
echo MySQL80 service is running.
echo.

echo [2/5] Configuring MySQL to accept remote connections...
set MYSQL_CONFIG=C:\ProgramData\MySQL\MySQL Server 8.0\my.ini

REM Check if config file exists
if not exist "%MYSQL_CONFIG%" (
    echo ERROR: MySQL configuration file not found at %MYSQL_CONFIG%
    pause
    exit /b 1
)

REM Create backup
echo Creating backup of my.ini...
copy "%MYSQL_CONFIG%" "%MYSQL_CONFIG%.backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%" >nul
echo Backup created.
echo.

REM Check current bind-address setting
findstr /C:"bind-address" "%MYSQL_CONFIG%" >nul
if %errorLevel% equ 0 (
    echo Found existing bind-address setting. Updating...
    powershell -Command "(Get-Content '%MYSQL_CONFIG%') -replace 'bind-address\s*=\s*127\.0\.0\.1', 'bind-address = 0.0.0.0' -replace 'bind-address\s*=\s*::1', 'bind-address = 0.0.0.0' | Set-Content '%MYSQL_CONFIG%'"
) else (
    echo Adding bind-address setting...
    REM Find [mysqld] section and add bind-address after it
    powershell -Command "$content = Get-Content '%MYSQL_CONFIG%'; $newContent = @(); $found = $false; foreach ($line in $content) { $newContent += $line; if ($line -match '\[mysqld\]' -and -not $found) { $newContent += 'bind-address = 0.0.0.0'; $found = $true } }; $newContent | Set-Content '%MYSQL_CONFIG%'"
)
echo Configuration updated.
echo.

echo [3/5] Restarting MySQL service...
net stop MySQL80
timeout /t 3 /nobreak >nul
net start MySQL80
timeout /t 5 /nobreak >nul
echo MySQL service restarted.
echo.

echo [4/5] Configuring Windows Firewall...
netsh advfirewall firewall show rule name="MySQL" >nul 2>&1
if %errorLevel% equ 0 (
    echo MySQL firewall rule already exists.
) else (
    echo Adding firewall rule for MySQL port 3306...
    netsh advfirewall firewall add rule name="MySQL" dir=in action=allow protocol=TCP localport=3306
    echo Firewall rule added.
)
echo.

echo [5/5] Displaying network information...
echo.
echo Your computer's IP addresses:
ipconfig | findstr /C:"IPv4"
echo.
echo IMPORTANT: Note your Wi-Fi IP address (usually 192.168.x.x)
echo This is the IP address other computers will use to connect.
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run the MySQL user setup script (setup_mysql_remote_user.sql)
echo 2. Update Django settings.py to use DB_HOST=127.0.0.1 on this computer
echo 3. Share your IP address with the remote computer
echo.
pause

