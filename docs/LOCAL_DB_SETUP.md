# 🗄️ Local PostgreSQL + PostGIS Setup for EchoSphere

**Complete step-by-step guide for setting up PostgreSQL with PostGIS locally (NO Docker required)**

Choose your operating system:
- [Windows](#-windows-setup)
- [macOS](#-macos-setup)
- [Linux](#-linux-setup)

---

## 🪟 Windows Setup

### Step 1: Download PostgreSQL

1. Visit the official PostgreSQL download page:
   **https://www.postgresql.org/download/windows/**

2. Click on **"Download the installer"** link (EnterpriseDB installer)

3. Download **PostgreSQL 15.x** for Windows (x86-64)
   - File size: ~300 MB
   - File name: `postgresql-15.x-windows-x64.exe`

### Step 2: Install PostgreSQL

1. **Run the installer** (`postgresql-15.x-windows-x64.exe`)
   - Right-click → "Run as administrator"

2. **Setup Wizard - Installation Directory**
   - Keep default: `C:\Program Files\PostgreSQL\15`
   - Click **Next**

3. **Select Components**
   - ✅ PostgreSQL Server
   - ✅ pgAdmin 4 (GUI tool)
   - ✅ Stack Builder (needed for PostGIS)
   - ✅ Command Line Tools
   - Click **Next**

4. **Data Directory**
   - Keep default: `C:\Program Files\PostgreSQL\15\data`
   - Click **Next**

5. **Set Superuser Password**
   - Enter a password for the `postgres` user
   - **IMPORTANT**: Remember this password!
   - Example: `postgres123` (use a strong password in production)
   - Click **Next**

6. **Port**
   - Keep default: `5432`
   - Click **Next**

7. **Locale**
   - Keep default: `[Default locale]`
   - Click **Next**

8. **Ready to Install**
   - Click **Next**
   - Wait for installation (2-3 minutes)

9. **Completing Setup**
   - ✅ Check "Launch Stack Builder at exit"
   - Click **Finish**

### Step 3: Install PostGIS via Stack Builder

1. **Stack Builder** will launch automatically

2. **Select Installation**
   - Choose: `PostgreSQL 15 (x64) on port 5432`
   - Click **Next**

3. **Select Applications**
   - Expand **"Spatial Extensions"**
   - ✅ Check **"PostGIS 3.3 Bundle for PostgreSQL 15"**
   - Click **Next**

4. **Download Directory**
   - Keep default download location
   - Click **Next**
   - Wait for download (100-200 MB)

5. **Install PostGIS**
   - Click **Next** to start installation
   - Click **Yes** to run installer
   - Accept license agreement
   - Keep all default options
   - Click **Next** through all screens
   - Wait for installation
   - Click **Close** when done

### Step 4: Add PostgreSQL to System PATH

1. **Open System Environment Variables**
   - Press `Win + R`
   - Type: `sysdm.cpl`
   - Press Enter

2. **Advanced Tab**
   - Click **"Environment Variables"** button

3. **Edit PATH**
   - Under "System variables", find and select **Path**
   - Click **Edit**
   - Click **New**
   - Add: `C:\Program Files\PostgreSQL\15\bin`
   - Click **OK** on all dialogs

4. **Verify PATH** (open new Command Prompt)
   ```cmd
   psql --version
   ```
   - Should show: `psql (PostgreSQL) 15.x`

### Step 5: Create EchoSphere Database

#### Option A: Using pgAdmin 4 (GUI)

1. **Open pgAdmin 4**
   - Search in Start Menu: "pgAdmin 4"
   - Enter your master password (first time setup)

2. **Connect to PostgreSQL**
   - Expand **Servers** in left sidebar
   - Click **PostgreSQL 15**
   - Enter password: (the one you set during installation)

3. **Create Database**
   - Right-click **Databases**
   - Select **Create** → **Database**
   - **Name**: `echosphere_db`
   - **Owner**: postgres
   - Click **Save**

4. **Create User**
   - Expand **Login/Group Roles**
   - Right-click → **Create** → **Login/Group Role**
   - **General Tab**:
     - Name: `echosphere`
   - **Definition Tab**:
     - Password: `echosphere_dev`
   - **Privileges Tab**:
     - ✅ Can login?
   - Click **Save**

5. **Grant Permissions**
   - Right-click `echosphere_db`
   - Select **Properties**
   - Go to **Security** tab
   - Click **+** to add
   - Select: `echosphere`
   - Privileges: Select **ALL**
   - Click **Save**

6. **Enable PostGIS**
   - Right-click `echosphere_db`
   - Select **Query Tool**
   - Run this SQL:
   ```sql
   CREATE EXTENSION IF NOT EXISTS postgis;
   ```
   - Click **Execute** (F5)
   - Should see: "CREATE EXTENSION"

7. **Verify PostGIS**
   - In Query Tool, run:
   ```sql
   SELECT PostGIS_Version();
   ```
   - Should show version like: "3.3 USE_GEOS=1..."

#### Option B: Using Command Line

1. **Open Command Prompt** (as Administrator)

2. **Connect to PostgreSQL**
   ```cmd
   psql -U postgres -h localhost
   ```
   - Enter your postgres password

3. **Create Database and User**
   ```sql
   -- Create database
   CREATE DATABASE echosphere_db;
   
   -- Create user
   CREATE USER echosphere WITH PASSWORD 'echosphere_dev';
   
   -- Grant permissions
   ALTER DATABASE echosphere_db OWNER TO echosphere;
   GRANT ALL PRIVILEGES ON DATABASE echosphere_db TO echosphere;
   
   -- Exit
   \q
   ```

4. **Enable PostGIS**
   ```cmd
   psql -U postgres -d echosphere_db -h localhost
   ```
   ```sql
   CREATE EXTENSION IF NOT EXISTS postgis;
   SELECT PostGIS_Version();
   \q
   ```

### Step 6: Verify Setup

```cmd
# Test connection
psql -U echosphere -d echosphere_db -h localhost

# You should see:
# Password for user echosphere: (enter: echosphere_dev)
# echosphere_db=>

# Test PostGIS
SELECT PostGIS_Version();

# Exit
\q
```

✅ **Windows setup complete!** Continue to [Final Steps](#-final-steps)

---

## 🍎 macOS Setup

### Step 1: Install Homebrew (if not installed)

```bash
# Check if Homebrew is installed
brew --version

# If not installed, install it:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install PostgreSQL and PostGIS

```bash
# Install PostgreSQL 15
brew install postgresql@15

# Install PostGIS
brew install postgis
```

### Step 3: Add PostgreSQL to PATH

```bash
# Add to your shell profile (~/.zshrc for zsh or ~/.bash_profile for bash)
echo 'export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc

# For Intel Macs, use:
# echo 'export PATH="/usr/local/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc

# Reload shell configuration
source ~/.zshrc
```

### Step 4: Start PostgreSQL Service

```bash
# Start PostgreSQL (will auto-start on boot)
brew services start postgresql@15

# Verify it's running
brew services list | grep postgresql

# Should show: postgresql@15  started
```

### Step 5: Create EchoSphere Database

```bash
# Connect to PostgreSQL (no password needed for local user)
psql postgres

# In psql prompt:
```
```sql
-- Create database
CREATE DATABASE echosphere_db;

-- Create user
CREATE USER echosphere WITH PASSWORD 'echosphere_dev';

-- Grant permissions
ALTER DATABASE echosphere_db OWNER TO echosphere;
GRANT ALL PRIVILEGES ON DATABASE echosphere_db TO echosphere;

-- Exit
\q
```

### Step 6: Enable PostGIS Extension

```bash
# Connect to echosphere_db
psql -d echosphere_db

# Enable PostGIS
```
```sql
CREATE EXTENSION IF NOT EXISTS postgis;

-- Verify PostGIS
SELECT PostGIS_Version();

-- Should show: 3.3.x USE_GEOS=1...

-- Exit
\q
```

### Step 7: Verify Setup

```bash
# Test connection with echosphere user
psql -U echosphere -d echosphere_db -h localhost

# Enter password when prompted: echosphere_dev

# Test PostGIS
SELECT PostGIS_Version();

# Exit
\q
```

### Optional: GUI Client (Postico)

```bash
# Install Postico (free PostgreSQL client for macOS)
brew install --cask postico

# Or download from: https://eggerapps.at/postico/
```

✅ **macOS setup complete!** Continue to [Final Steps](#-final-steps)

---

## 🐧 Linux Setup

### Ubuntu / Debian

#### Step 1: Update System

```bash
sudo apt update
sudo apt upgrade -y
```

#### Step 2: Install PostgreSQL and PostGIS

```bash
# Install PostgreSQL 15 and PostGIS
sudo apt install -y postgresql-15 postgresql-contrib-15 postgis postgresql-15-postgis-3

# For Ubuntu 22.04 or newer, you might need to add PostgreSQL repo first:
# sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
# wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
# sudo apt update
# Then install as above
```

#### Step 3: Start PostgreSQL Service

```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Enable auto-start on boot
sudo systemctl enable postgresql

# Check status
sudo systemctl status postgresql

# Should show: active (running)
```

#### Step 4: Create EchoSphere Database

```bash
# Switch to postgres user
sudo -u postgres psql

# In psql prompt:
```
```sql
-- Create database
CREATE DATABASE echosphere_db;

-- Create user
CREATE USER echosphere WITH PASSWORD 'echosphere_dev';

-- Grant permissions
ALTER DATABASE echosphere_db OWNER TO echosphere;
GRANT ALL PRIVILEGES ON DATABASE echosphere_db TO echosphere;

-- Exit
\q
```

#### Step 5: Enable PostGIS Extension

```bash
# Connect to echosphere_db as postgres
sudo -u postgres psql -d echosphere_db

# Enable PostGIS
```
```sql
CREATE EXTENSION IF NOT EXISTS postgis;

-- Verify PostGIS
SELECT PostGIS_Version();

-- Exit
\q
```

#### Step 6: Configure PostgreSQL for Local Development

```bash
# Edit pg_hba.conf to allow password authentication
sudo nano /etc/postgresql/15/main/pg_hba.conf

# Find the line:
# local   all             all                                     peer

# Change to:
# local   all             all                                     md5

# Save and exit (Ctrl+X, Y, Enter)

# Restart PostgreSQL
sudo systemctl restart postgresql
```

#### Step 7: Verify Setup

```bash
# Test connection
psql -U echosphere -d echosphere_db -h localhost

# Enter password: echosphere_dev

# Test PostGIS
SELECT PostGIS_Version();

# Exit
\q
```

### Fedora / RHEL / CentOS

```bash
# Install PostgreSQL 15
sudo dnf install -y postgresql15-server postgresql15-contrib postgis33_15

# Initialize database
sudo postgresql-15-setup initdb

# Start and enable service
sudo systemctl start postgresql-15
sudo systemctl enable postgresql-15

# Follow same steps as Ubuntu for creating database and user
```

### Arch Linux

#### Step 1: Install PostgreSQL and PostGIS

```bash
# Install PostgreSQL and PostGIS
sudo pacman -S postgresql postgis
```

#### Step 2: Initialize Database Cluster

```bash
# Initialize database
sudo -u postgres initdb -D /var/lib/postgres/data
```

#### Step 3: Configure Authentication

```bash
# Edit pg_hba.conf for password authentication
sudo nano /var/lib/postgres/data/pg_hba.conf

# Find these lines:
# local   all             all                                     peer
# host    all             all             127.0.0.1/32            ident

# Change to:
# local   all             all                                     md5
# host    all             all             127.0.0.1/32            md5

# Save and exit (Ctrl+X, Y, Enter)
```

#### Step 4: Start PostgreSQL Service

```bash
# Start and enable service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Check status
sudo systemctl status postgresql
```

#### Step 5: Create Database and User

```bash
# Switch to postgres user
sudo -u postgres psql

# In psql prompt:
```
```sql
-- Create database
CREATE DATABASE echosphere_db;

-- Create user
CREATE USER echosphere WITH PASSWORD 'echosphere_dev';

-- Grant permissions
ALTER DATABASE echosphere_db OWNER TO echosphere;
GRANT ALL PRIVILEGES ON DATABASE echosphere_db TO echosphere;

-- Exit
\q
```

#### Step 6: Enable PostGIS

```bash
# Connect to database
sudo -u postgres psql -d echosphere_db

# Enable PostGIS
```
```sql
CREATE EXTENSION IF NOT EXISTS postgis;

-- Verify
SELECT PostGIS_Version();

-- Exit
\q
```

#### Step 7: Verify Setup

```bash
# Test connection with echosphere user
psql -U echosphere -d echosphere_db -h localhost

# Enter password: echosphere_dev
# Test PostGIS
SELECT PostGIS_Version();

# Exit
\q
```

✅ **Linux setup complete!** Continue to [Final Steps](#-final-steps)

---

## ✅ Final Steps

### 1. Configure EchoSphere Backend

Create or update `backend/.env`:

```bash
cd backend
cp .env.example .env
nano .env  # or use your preferred editor
```

Add/update these lines:

```env
# Database Configuration
DB_USER=echosphere
DB_PASSWORD=echosphere_dev
DB_HOST=localhost
DB_PORT=5432
DB_NAME=echosphere_db

# API Keys (add your actual keys)
OPENROUTER_API_KEY=your_openrouter_key_here
NASA_API_KEY=your_nasa_key_here
```

### 2. Install Python Dependencies

```bash
cd backend

# Install database requirements
pip install -r requirements/database.txt

# Or install all requirements
pip install -r requirements/linux.txt -r requirements/database.txt
```

### 3. Initialize Database

```bash
cd backend

# Run initialization script
python init_db.py

# You'll be prompted:
# - Drop existing tables? (y/N) → Enter 'y' for first setup
# - Clear existing cities and reseed? (y/N) → Enter 'y'

# This will:
# ✅ Create all 9 database tables
# ✅ Enable PostGIS extension
# ✅ Seed 8 Malaysian city presets
# ✅ Verify database setup
```

### 4. Verify Everything Works

```bash
# Start the backend server
cd backend
python main.py

# Should see:
# 🚀 Echosphere Backend Starting...
# 📍 Backend URL: http://localhost:8000
# ...
# ✅ PostGIS available: 3.3.x...
```

Open your browser and check:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

Health check should return:
```json
{
  "status": "ok",
  "database": "healthy",
  "postgis": "healthy",
  "services": {
    "api": "operational",
    "openrouter": "operational",
    "nasa": "operational"
  }
}
```

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: "psql: command not found"

**Solution:**
- **Windows**: Add PostgreSQL bin folder to PATH (see Step 4)
- **macOS**: Add PostgreSQL to PATH in shell profile
- **Linux**: Install postgresql-client: `sudo apt install postgresql-client`

#### Issue: "connection refused" or "could not connect to server"

**Solutions:**
1. Check if PostgreSQL is running:
   ```bash
   # Windows (Command Prompt as admin)
   sc query postgresql-x64-15
   
   # macOS
   brew services list
   
   # Linux
   sudo systemctl status postgresql
   ```

2. Start PostgreSQL if not running:
   ```bash
   # Windows (Command Prompt as admin)
   net start postgresql-x64-15
   
   # macOS
   brew services start postgresql@15
   
   # Linux
   sudo systemctl start postgresql
   ```

3. Check port 5432 is not in use:
   ```bash
   # Windows
   netstat -an | findstr :5432
   
   # macOS/Linux
   lsof -i :5432
   ```

#### Issue: "password authentication failed for user"

**Solutions:**
1. Verify password:
   ```bash
   psql -U echosphere -d echosphere_db -h localhost
   # Password: echosphere_dev
   ```

2. Reset password:
   ```sql
   # Connect as postgres
   psql -U postgres
   
   # Reset password
   ALTER USER echosphere WITH PASSWORD 'echosphere_dev';
   ```

#### Issue: "database echosphere_db does not exist"

**Solution:**
```sql
# Connect as postgres
psql -U postgres

# Create database
CREATE DATABASE echosphere_db;
ALTER DATABASE echosphere_db OWNER TO echosphere;
GRANT ALL PRIVILEGES ON DATABASE echosphere_db TO echosphere;
```

#### Issue: "PostGIS extension not found"

**Solutions:**
1. **Windows**: Reinstall PostGIS via Stack Builder
2. **macOS**: `brew install postgis`
3. **Linux**: `sudo apt install postgresql-15-postgis-3`

Then enable it:
```sql
psql -U postgres -d echosphere_db
CREATE EXTENSION IF NOT EXISTS postgis;
```

#### Issue: "Permission denied" errors on Linux

**Solution:**
```bash
# Make sure your user is in postgres group
sudo usermod -a -G postgres $USER

# Or run commands with sudo
sudo -u postgres psql
```

### Arch Linux Specific Issues

#### Issue: "peer authentication failed for user echosphere"

**Solution:**
```bash
# Edit pg_hba.conf
sudo nano /var/lib/postgres/data/pg_hba.conf

# Change 'peer' to 'md5' for local connections:
# Before:
# local   all             all                                     peer

# After:
# local   all             all                                     md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

#### Issue: PostgreSQL service won't start

**Solution:**
```bash
# Check logs for errors
sudo journalctl -u postgresql -n 50

# Common fix: Reinitialize database cluster
sudo systemctl stop postgresql
sudo rm -rf /var/lib/postgres/data
sudo -u postgres initdb -D /var/lib/postgres/data

# Reconfigure authentication (see above)
# Then start service
sudo systemctl start postgresql
```

#### Issue: "could not connect to server: No such file or directory"

**Solution:**
```bash
# Check if socket directory exists
ls -la /run/postgresql/

# If missing, create it:
sudo mkdir -p /run/postgresql
sudo chown postgres:postgres /run/postgresql

# Restart service
sudo systemctl restart postgresql
```

### Windows Specific Issues

#### Issue: Can't find psql command after installation

**Solution:**
1. **Add PostgreSQL to PATH:**
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Click **Advanced** → **Environment Variables**
   - Under "System variables", find and edit **Path**
   - Click **New** and add: `C:\Program Files\PostgreSQL\15\bin`
   - Click **OK** on all dialogs
   - **Restart Command Prompt** or PowerShell

2. **Verify:**
   ```cmd
   psql --version
   ```

#### Issue: PostGIS extension not found in pgAdmin

**Solution:**
1. Open **Stack Builder** (from Start Menu)
2. Select your PostgreSQL installation
3. Expand **Spatial Extensions**
4. Select **PostGIS 3.3 Bundle**
5. Install and restart pgAdmin

#### Issue: "Access Denied" errors in Windows

**Solution:**
1. **Run as Administrator:**
   - Right-click Command Prompt or PowerShell
   - Select "Run as administrator"

2. **Check User Privileges:**
   ```sql
   -- Connect as postgres
   psql -U postgres
   
   -- Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE echosphere_db TO echosphere;
   ```

3. **Firewall Issues:**
   - Windows Firewall might block PostgreSQL
   - Add exception for port 5432
   - Or temporarily disable firewall for testing

#### Issue: pgAdmin can't connect to localhost

**Solution:**
1. **Check PostgreSQL service is running:**
   - Press `Win + R`, type `services.msc`
   - Find "postgresql-x64-15"
   - Status should be "Running"
   - If not, right-click → Start

2. **Check connection settings in pgAdmin:**
   - Host: `localhost` or `127.0.0.1`
   - Port: `5432`
   - Username: `postgres` or `echosphere`
   - Database: `echosphere_db`

---

## 🔍 Verification Installation Checklist

Run these commands to verify your setup is complete:

### 1. Connect to Database

```bash
psql -U echosphere -d echosphere_db -h localhost
# Password: echosphere_dev
```

### 2. Check PostgreSQL Version

```sql
SELECT version();
```

**Expected output:** `PostgreSQL 15.x on x86_64...`

### 3. Check PostGIS Version

```sql
SELECT PostGIS_Version();
```

**Expected output:** `3.3.x USE_GEOS=1 USE_PROJ=1...`

### 4. Test PostGIS Functions

```sql
-- Create a test point (Boston, MA)
SELECT ST_AsText(ST_MakePoint(-71.1043, 42.3150));
```

**Expected output:** `POINT(-71.1043 42.315)`

### 5. Test Geometry Operations

```sql
-- Calculate distance between two points (in degrees)
SELECT ST_Distance(
    ST_MakePoint(-71.1043, 42.3150),  -- Boston
    ST_MakePoint(-74.0060, 40.7128)   -- New York
) AS distance;
```

**Expected output:** `~2.9` (degrees)

### 6. List All Databases

```sql
\l
```

**Expected:** Should see `echosphere_db` in the list

### 7. List All Users

```sql
\du
```

**Expected:** Should see `echosphere` user with appropriate roles

### 8. Check Current Database

```sql
SELECT current_database();
```

**Expected output:** `echosphere_db`

### 9. Check Current User

```sql
SELECT current_user;
```

**Expected output:** `echosphere`

### 10. Verify Database Tables Will Be Created

```sql
-- Check if we can create a test table
CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(50));
INSERT INTO test_table (name) VALUES ('test');
SELECT * FROM test_table;
DROP TABLE test_table;
```

**Expected:** No errors, should create, insert, select, and drop successfully

### 11. Exit psql

```sql
\q
```

---

## ✅ Installation Success Criteria

Your installation is successful if:

- ✅ PostgreSQL version is 15.x
- ✅ PostGIS version is 3.3.x
- ✅ PostGIS functions work (ST_MakePoint, ST_AsText, etc.)
- ✅ `echosphere_db` database exists
- ✅ `echosphere` user exists
- ✅ Can connect without errors
- ✅ Can create and drop tables
- ✅ Geometry types work correctly

If all checks pass, you're ready to proceed! 🎉

---

## 📋 Quick Command Reference

### Common psql Commands

```bash
# Connect to database
psql -U echosphere -d echosphere_db -h localhost

# Connect as postgres superuser
psql -U postgres

# Connect and run single command
psql -U echosphere -d echosphere_db -h localhost -c "SELECT version();"

# Run SQL file
psql -U echosphere -d echosphere_db -h localhost -f script.sql
```

### Inside psql

```sql
-- List all databases
\l

-- List all tables
\dt

-- Describe table structure
\d table_name

-- List all users/roles
\du

-- List all schemas
\dn

-- Show current database
SELECT current_database();

-- Show current user
SELECT current_user;

-- Get database size
SELECT pg_size_pretty(pg_database_size('echosphere_db'));

-- Show all PostGIS functions
\df ST_*

-- Get help
\?

-- Exit
\q
```

### Verify Database Schema

```bash
# Connect to database
psql -U echosphere -d echosphere_db -h localhost

# List all tables
\dt

# Should show 9 tables:
# - users
# - selected_areas
# - environmental_metrics
# - area_analyses
# - chat_messages
# - nasa_cache
# - disaster_events
# - city_presets

# Check PostGIS
SELECT PostGIS_Version();

# List city presets
SELECT name, country, population FROM city_presets;

# Should show 8 Malaysian cities

# Exit
\q
```

---

## 📚 Additional Resources

### PostgreSQL Documentation
- **Official Docs**: https://www.postgresql.org/docs/15/
- **Tutorial**: https://www.postgresqltutorial.com/

### PostGIS Documentation
- **Official Docs**: https://postgis.net/documentation/
- **Tutorial**: https://postgis.net/workshops/postgis-intro/

### GUI Tools

**Windows:**
- pgAdmin 4 (included with PostgreSQL)
- DBeaver: https://dbeaver.io/

**macOS:**
- Postico: https://eggerapps.at/postico/
- TablePlus: https://tableplus.com/

**Linux:**
- pgAdmin 4: `sudo apt install pgadmin4`
- DBeaver: https://dbeaver.io/

### Useful Commands

```bash
# Connect to database
psql -U echosphere -d echosphere_db -h localhost

# List all databases
\l

# List all tables
\dt

# Describe table structure
\d table_name

# List all users/roles
\du

# Execute SQL file
\i filename.sql

# Show current database
SELECT current_database();

# Show current user
SELECT current_user;

# Get database size
SELECT pg_size_pretty(pg_database_size('echosphere_db'));

# Exit
\q
```

---

## 🎉 Success!

You've successfully set up PostgreSQL + PostGIS for EchoSphere development!

**What's Configured:**
- ✅ PostgreSQL 15 running
- ✅ PostGIS 3.3 extension enabled
- ✅ `echosphere_db` database created
- ✅ `echosphere` user with full permissions
- ✅ Ready for EchoSphere application

---

## 🚀 Next Steps

### 1. Update Backend Configuration

Navigate to backend directory and configure environment:

```bash
cd backend

# Copy example environment file
cp .env.example .env

# Edit with your preferred editor
nano .env  # or: code .env, vim .env, etc.
```

Update the following in `.env`:

```env
# Database Configuration
DB_USER=echosphere
DB_PASSWORD=echosphere_dev
DB_HOST=localhost
DB_PORT=5432
DB_NAME=echosphere_db

# API Keys (get your actual keys)
OPENROUTER_API_KEY=your_openrouter_key_here
NASA_API_KEY=your_nasa_key_here
```

### 2. Install Python Dependencies

```bash
cd backend

# Install all requirements
pip install -r requirements/linux.txt
pip install -r requirements/database.txt

# Or install to custom directory
pip install --target=../.venv-packages -r requirements/linux.txt
pip install --target=../.venv-packages -r requirements/database.txt
```

**Required packages:**
- SQLAlchemy 2.0+ (ORM)
- psycopg2-binary (PostgreSQL driver)
- alembic (migrations)
- geoalchemy2 (PostGIS support)
- FastAPI, uvicorn (web framework)
- pydantic, pydantic-settings (validation)

### 3. Initialize Database Schema

Run the initialization script to create tables and seed data:

```bash
cd backend

python init_db.py
```

**What it does:**
- ✅ Checks database connection
- ✅ Verifies PostGIS is available
- ✅ Creates all 9 database tables
- ✅ Seeds 8 Malaysian city presets (Sibu, Kuala Lumpur, etc.)
- ✅ Verifies database setup

**Prompts you'll see:**
```
Drop existing tables and recreate? (y/N): y
Clear existing cities and reseed? (y/N): y
```

Enter `y` for first-time setup.

### 4. Run Database Migrations (Alternative)

If you prefer using Alembic migrations:

```bash
cd backend

# Check current migration status
alembic current

# Apply all migrations
alembic upgrade head

# Verify tables were created
psql -U echosphere -d echosphere_db -h localhost -c "\dt"
```

### 5. Start the Backend Server

```bash
cd backend

python main.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
🚀 Echosphere Backend Starting...
📍 Backend URL: http://localhost:8000
🤖 AI Model: deepseek/deepseek-chat-v3.1:free
🛰️  NASA API: Configured
✅ PostGIS available: 3.3.x...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 6. Test the API

Open your browser and visit:

**API Documentation:**
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

**Health Check:**
- http://localhost:8000/api/health

Expected response:
```json
{
  "status": "ok",
  "database": "healthy",
  "postgis": "healthy",
  "services": {
    "api": "operational",
    "openrouter": "operational",
    "nasa": "operational"
  }
}
```

### 7. Test Database Queries

Try some example queries from Python:

```python
# Test script: test_db.py
from app.database import get_db_context
from app.crud import get_or_create_user, get_all_city_presets

# Test user creation
with get_db_context() as db:
    user = get_or_create_user(db, session_id="test_user_123")
    print(f"✅ Created user: {user.id}")
    
    # Test city presets
    cities = get_all_city_presets(db)
    print(f"✅ Found {len(cities)} cities")
    for city in cities:
        print(f"   - {city.name}, {city.country}")
```

Run the test:
```bash
cd backend
python test_db.py
```

### 8. Start Frontend (Optional)

If you want to test the full stack:

```bash
cd frontend-react

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: http://localhost:5173

---

## 📚 Additional Documentation

Now that your database is set up, explore these resources:

### Database Documentation
- **[DATABASE_README.md](../backend/DATABASE_README.md)** - Schema overview & quick reference
- **[USAGE_EXAMPLES.md](../backend/USAGE_EXAMPLES.md)** - 50+ code examples
- **[DATABASE_SETUP.md](../backend/DATABASE_SETUP.md)** - Full setup guide with Render deployment

### Application Documentation
- **[README.md](../README.md)** - Main project README
- **[QUICKSTART.md](../backend/QUICKSTART.md)** - Backend quick start
- **[DEPLOYMENT.md](../DEPLOYMENT.md)** - Production deployment guide

### Development Resources
- **API Docs**: http://localhost:8000/docs (when server is running)
- **Database Schema**: See `backend/app/models/db_models.py`
- **CRUD Operations**: See `backend/app/crud.py`
- **Migrations**: See `backend/alembic/versions/`

---

## 🎓 Learning Resources

### PostgreSQL
- **Official Tutorial**: https://www.postgresqltutorial.com/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/15/
- **Performance Tuning**: https://wiki.postgresql.org/wiki/Performance_Optimization

### PostGIS
- **PostGIS Workshop**: https://postgis.net/workshops/postgis-intro/
- **PostGIS Docs**: https://postgis.net/documentation/
- **Spatial Queries**: https://postgis.net/docs/reference.html

### Python + PostgreSQL
- **SQLAlchemy Tutorial**: https://docs.sqlalchemy.org/en/20/tutorial/
- **Alembic Tutorial**: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- **FastAPI + Databases**: https://fastapi.tiangolo.com/tutorial/sql-databases/

---

## 🐛 Getting Help

### Check Logs

If something goes wrong, check these logs:

**PostgreSQL Logs:**
```bash
# Linux
sudo tail -f /var/log/postgresql/postgresql-15-main.log

# Arch Linux
sudo journalctl -u postgresql -f

# macOS (Homebrew)
tail -f /opt/homebrew/var/log/postgresql@15.log

# Windows
# Check: C:\Program Files\PostgreSQL\15\data\log\
```

**EchoSphere Backend Logs:**
```bash
# Check terminal output where you ran python main.py
# Or check application logs
tail -f /tmp/echosphere-backend.log
```

### Common Next Steps Issues

**Issue: "Module not found" errors**
```bash
# Reinstall dependencies
pip install -r requirements/linux.txt -r requirements/database.txt
```

**Issue: "Cannot connect to database" in Python**
```python
# Verify connection string in .env
DB_USER=echosphere
DB_PASSWORD=echosphere_dev
DB_HOST=localhost  # NOT 127.0.0.1 on some systems
DB_PORT=5432
DB_NAME=echosphere_db
```

**Issue: "Tables already exist" when running init_db.py**
```bash
# Drop and recreate (CAUTION: Deletes all data)
python init_db.py
# When prompted "Drop existing tables?", enter: y
```

**Issue: Alembic migrations fail**
```bash
# Reset migrations
cd backend
rm alembic/versions/*.py  # Keep only __init__.py if present
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

---

## ✅ Development Workflow

Your typical development cycle:

1. **Start Database** (if not auto-starting)
   ```bash
   # Linux
   sudo systemctl start postgresql
   
   # macOS
   brew services start postgresql@15
   
   # Windows - it auto-starts, or use services.msc
   ```

2. **Start Backend**
   ```bash
   cd backend
   python main.py
   ```

3. **Start Frontend** (optional)
   ```bash
   cd frontend-react
   npm run dev
   ```

4. **Make Changes**
   - Edit code
   - Backend auto-reloads (uvicorn --reload)
   - Frontend auto-reloads (Vite HMR)

5. **Test Changes**
   - Visit http://localhost:8000/docs
   - Test API endpoints
   - Check frontend at http://localhost:5173

6. **Database Changes?**
   ```bash
   # Create migration
   alembic revision --autogenerate -m "Your change"
   
   # Apply migration
   alembic upgrade head
   ```

7. **Stop Servers**
   ```bash
   # Ctrl+C in terminal where servers are running
   
   # Or use commands:
   pkill -f "python main.py"
   pkill -f "npm run dev"
   ```

---

## 🎉 You're All Set!

Congratulations! Your EchoSphere development environment is ready.

**What you've accomplished:**
- ✅ PostgreSQL 15 + PostGIS 3.3 installed
- ✅ Database created and configured
- ✅ EchoSphere schema initialized
- ✅ Sample data loaded (8 Malaysian cities)
- ✅ Ready to start developing!

**Quick Links:**
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173
- **Database**: `psql -U echosphere -d echosphere_db -h localhost`

**Next:** Start building features for urban resilience analysis! 🌍

---

**Built for NASA Space Apps Challenge 2025** 🚀🌍

**Focus Area**: Sibu & Sibu Jaya, Sarawak, Malaysia

**Database**: PostgreSQL 15 + PostGIS 3.3  
**Backend**: FastAPI + SQLAlchemy 2.0  
**Frontend**: React + Vite + Leaflet.js

