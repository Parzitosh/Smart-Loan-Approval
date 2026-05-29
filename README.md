# FinTech Credit Risk Analytics Engine

A high-performance PySpark and FastAPI-based credit risk assessment engine with AWS RDS PostgreSQL persistence for batch processing loan applications.

## Features

- **Batch Processing**: Process multiple loan applications simultaneously using PySpark
- **Risk Calculation**: Automated debt-to-income ratio and credit risk assessment
- **Interest Rate Computation**: Dynamic interest rates based on risk profile
- **Database Persistence**: Automatic persistence to AWS RDS PostgreSQL via PySpark JDBC writer
- **History Retrieval**: Fetch processed records with fast psycopg2 queries
- **RESTful API**: FastAPI endpoints for easy integration
- **Distributed Computing**: PySpark with vectorized SQL operations
- **Type Safety**: Pydantic models for request/response validation

## Prerequisites

- Python 3.8+
- Java 8+ (for PySpark)
- PostgreSQL (local or AWS RDS)

## Installation

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Configure Database** (see [DATABASE_SETUP.md](DATABASE_SETUP.md)):

```bash
export DB_HOST=your-rds-endpoint.rds.amazonaws.com
export DB_PORT=5432
export DB_USER=postgres
export DB_PASSWORD=your-password
export DB_NAME=fintech_analytics
```

## Running the Server

Start the FastAPI server:

```bash
python main.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### POST `/api/process-risk`

Process multiple loan applications for credit risk assessment and persist to PostgreSQL.

**Request Body:**

```json
[
  {
    "applicationId": "APP001",
    "income": 60000,
    "monthlyDebt": 2500,
    "creditScore": 720,
    "applicantName": "John Doe"
  },
  {
    "applicationId": "APP002",
    "income": 45000,
    "monthlyDebt": 3000,
    "creditScore": 580,
    "applicantName": "Jane Smith"
  }
]
```

**Response:**

```json
[
  {
    "applicationId": "APP001",
    "income": 60000,
    "monthlyDebt": 2500,
    "creditScore": 720,
    "debtToIncomeRatio": 0.5,
    "riskStatus": "Rejected",
    "interestRate": 0.0,
    "applicantName": "John Doe"
  },
  {
    "applicationId": "APP002",
    "income": 45000,
    "monthlyDebt": 3000,
    "creditScore": 580,
    "debtToIncomeRatio": 0.8,
    "riskStatus": "Rejected",
    "interestRate": 0.0,
    "applicantName": "Jane Smith"
  }
]
```

**Process Flow:**

1. Receives JSON array of applications
2. Creates PySpark DataFrame from input
3. Calculates DTI, RiskStatus, and InterestRate using Spark SQL functions
4. Persists results to PostgreSQL `credit_analytics` table via JDBC writer
5. Returns processed results immediately

### GET `/api/history`

Retrieve the last 50 processed records from the database.

**Response:**

```json
[
  {
    "id": 1,
    "applicationId": "APP001",
    "income": 60000.0,
    "monthlyDebt": 2500.0,
    "creditScore": 720,
    "debtToIncomeRatio": 0.5,
    "riskStatus": "Rejected",
    "interestRate": 0.0,
    "applicantName": "John Doe",
    "processed_at": "2026-05-27 14:30:45"
  },
  {
    "id": 2,
    "applicationId": "APP002",
    "income": 45000.0,
    "monthlyDebt": 3000.0,
    "creditScore": 580,
    "debtToIncomeRatio": 0.8,
    "riskStatus": "Rejected",
    "interestRate": 0.0,
    "applicantName": "Jane Smith",
    "processed_at": "2026-05-27 14:30:45"
  }
]
```

### GET `/health`

Health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "service": "FinTech Credit Risk Analytics Engine"
}
```

## Risk Assessment Logic

1. **Debt-to-Income Ratio (DTI)**: `monthlyDebt / (income / 12)`
2. **Risk Status**:
   - **Rejected**: If `creditScore < 600` OR `DTI > 0.45`
   - **Approved**: Otherwise
3. **Interest Rate**:
   - **Approved**: `0.05 + (0.10 * DTI)`
   - **Rejected**: `0.0`

## Database Schema

The `credit_analytics` table automatically created with:

```sql
CREATE TABLE credit_analytics (
    id SERIAL PRIMARY KEY,
    application_id VARCHAR(255) NOT NULL,
    income FLOAT NOT NULL,
    monthly_debt FLOAT NOT NULL,
    credit_score INT NOT NULL,
    debt_to_income_ratio FLOAT NOT NULL,
    risk_status VARCHAR(50) NOT NULL,
    interest_rate FLOAT NOT NULL,
    applicant_name VARCHAR(255),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Testing

Run the comprehensive test suite:

```bash
python test_api.py
```

Tests cover:

- Health check endpoint
- Risk processing with batch data
- History retrieval from database

## Architecture

### Technology Stack

- **API Framework**: FastAPI with Uvicorn
- **Processing Engine**: PySpark with DataFrame operations
- **Data Processing**: PySpark SQL functions for vectorized operations
- **Database**: PostgreSQL with JDBC writer for persistence
- **Connection Management**: psycopg2 for history queries
- **Type Safety**: Pydantic models for request/response validation

### Data Flow

```
JSON Input → PySpark DataFrame → SQL Transformations
                                    ↓
                          PostgreSQL JDBC Write
                                    ↓
                          Return Results + Store
```

## Environment Variables

| Variable    | Default           | Description              |
| ----------- | ----------------- | ------------------------ |
| DB_HOST     | localhost         | PostgreSQL host/endpoint |
| DB_PORT     | 5432              | PostgreSQL port          |
| DB_USER     | postgres          | Database user            |
| DB_PASSWORD | password          | Database password        |
| DB_NAME     | fintech_analytics | Database name            |

## Performance Considerations

- **PySpark JDBC Writer**: Automatically downloads PostgreSQL JDBC driver
- **Batch Processing**: Efficient bulk insertion via Spark DataFrames
- **Connection Pooling**: New connections for each request (production: implement pooling)
- **Distributed Computing**: Multi-core utilization on local machine
- **Vectorized Operations**: Spark SQL functions provide columnar optimization

## Production Deployment

1. **Use AWS RDS PostgreSQL** with automated backups
2. **Implement Connection Pooling** (e.g., PgBouncer)
3. **Enable SSL/TLS** for database connections
4. **Monitor Performance** with CloudWatch metrics
5. **Use AWS Secrets Manager** for credentials
6. **Implement Rate Limiting** in FastAPI
7. **Enable Logging** for audit trails

See [DATABASE_SETUP.md](DATABASE_SETUP.md) for detailed setup instructions.

## Troubleshooting

### Database Connection Issues

- Verify environment variables are set correctly
- Check PostgreSQL is running and accessible
- For AWS RDS, ensure security group allows port 5432

### JDBC Driver Download Timeout

- Check internet connectivity
- First run may take longer for dependency download
- Set Spark Jars packages manually if offline

### Table Creation Failed

- Ensure database user has DDL permissions
- Verify credentials with `psql` connection

See [DATABASE_SETUP.md](DATABASE_SETUP.md) for comprehensive troubleshooting guide.
