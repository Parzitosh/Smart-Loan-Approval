# Database Setup and Configuration Guide

## Prerequisites

1. **PostgreSQL Database** (Local or AWS RDS)
2. **Python 3.8+**
3. **Java 8+** (for PySpark)

## Environment Variables

Set these environment variables before running the FastAPI server:

### On Linux/macOS:

```bash
export DB_HOST=your-database-host
export DB_PORT=5432
export DB_USER=postgres
export DB_PASSWORD=your-secure-password
export DB_NAME=fintech_analytics
```

### On Windows (PowerShell):

```powershell
$env:DB_HOST = "your-database-host"
$env:DB_PORT = "5432"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "your-secure-password"
$env:DB_NAME = "fintech_analytics"
```

### On Windows (Command Prompt):

```cmd
set DB_HOST=your-database-host
set DB_PORT=5432
set DB_USER=postgres
set DB_PASSWORD=your-secure-password
set DB_NAME=fintech_analytics
```

## Local PostgreSQL Setup

### 1. Install PostgreSQL

**On macOS:**

```bash
brew install postgresql
brew services start postgresql
```

**On Linux (Ubuntu/Debian):**

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**On Windows:**
Download from https://www.postgresql.org/download/windows/

### 2. Create Database and User

```bash
psql -U postgres

# Inside psql:
CREATE DATABASE fintech_analytics;
CREATE USER postgres WITH PASSWORD 'password';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET default_transaction_deferrable TO on;
ALTER ROLE postgres SET default_time_zone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE fintech_analytics TO postgres;
\q
```

## AWS RDS PostgreSQL Setup

### 1. Create RDS Instance

1. Go to AWS RDS Console
2. Click "Create database"
3. Choose PostgreSQL
4. Select "Free tier" template (if eligible)
5. Configure:
   - DB Instance Identifier: `fintech-analytics-db`
   - Master username: `postgres`
   - Master password: (create a strong password)
6. Under "Connectivity", ensure public accessibility is enabled
7. Create a security group allowing inbound traffic on port 5432
8. Click "Create database"

### 2. Get Connection Details

After creation, note:

- **Endpoint**: Available in the RDS console (e.g., `fintech-db.xxxxx.us-east-1.rds.amazonaws.com`)
- **Port**: `5432` (default)
- **Username**: `postgres`
- **Password**: (what you set during creation)

### 3. Connect and Create Database

```bash
psql -h fintech-db.xxxxx.us-east-1.rds.amazonaws.com \
     -U postgres \
     -d postgres

# Inside psql:
CREATE DATABASE fintech_analytics;
\q
```

### 4. Set Environment Variables

```bash
export DB_HOST=fintech-db.xxxxx.us-east-1.rds.amazonaws.com
export DB_PORT=5432
export DB_USER=postgres
export DB_PASSWORD=your-password
export DB_NAME=fintech_analytics
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

### Process Risk Assessment (Batch)

```bash
curl -X POST http://localhost:8000/api/process-risk \
  -H "Content-Type: application/json" \
  -d '[
    {
      "applicationId": "APP001",
      "income": 60000,
      "monthlyDebt": 2500,
      "creditScore": 720,
      "applicantName": "John Doe"
    }
  ]'
```

### Get History (Last 50 Records)

```bash
curl http://localhost:8000/api/history
```

## Testing

Run the test suite:

```bash
python test_api.py
```

## Troubleshooting

### Connection Refused

- Ensure PostgreSQL is running
- Check DB_HOST and DB_PORT environment variables
- Verify firewall rules (for RDS)

### JDBC Driver Issues

- PySpark will automatically download the PostgreSQL JDBC driver
- First run may take longer due to dependency download
- Check internet connectivity

### Table Creation Failed

- Ensure the database user has DDL permissions
- Verify DB_USER has role permissions on the database

### Permission Denied

- Check database credentials in environment variables
- Verify user has appropriate permissions in PostgreSQL

## Performance Considerations

- **Batch Processing**: The endpoint accepts arrays for efficient bulk processing
- **PySpark**: Utilizes distributed computing (local multi-core)
- **Connection Pooling**: Each request creates a new connection for history endpoint
- **JDBC Writer**: Uses append mode for scalability

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** or AWS Secrets Manager
3. **Enable SSL/TLS** for RDS connections
4. **Restrict security groups** to necessary IP ranges
5. **Use strong passwords** for database users
6. **Rotate credentials** periodically

## Production Deployment

For production:

1. Use managed PostgreSQL (AWS RDS)
2. Enable automated backups
3. Use VPC for isolation
4. Implement connection pooling (e.g., PgBouncer)
5. Monitor performance with CloudWatch
6. Use parameter groups for configuration management
