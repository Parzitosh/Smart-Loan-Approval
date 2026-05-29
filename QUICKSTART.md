# FinTech Credit Risk Analytics Engine - Complete Setup Guide

A production-ready full-stack application combining **PySpark batch processing**, **FastAPI backend**, and **React dashboard** for credit risk assessment.

## 📋 Project Structure

```
fintech-credit-risk-engine/
├── Backend (Python/PySpark)
│   ├── main.py                      # FastAPI + PySpark application
│   ├── requirements.txt             # Python dependencies
│   ├── test_api.py                 # API test suite
│   ├── DATABASE_SETUP.md           # PostgreSQL setup guide
│   └── README.md                   # Backend documentation
│
├── Frontend (React/Tailwind)
│   ├── CreditRiskDashboard.jsx     # Main React component
│   ├── App.jsx                     # App wrapper
│   ├── main.jsx                    # React entry point
│   ├── index.html                  # HTML template
│   ├── index.css                   # Tailwind styles
│   ├── package.json                # npm dependencies
│   ├── vite.config.js              # Vite configuration
│   ├── tailwind.config.js          # Tailwind configuration
│   ├── postcss.config.js           # PostCSS configuration
│   ├── .eslintrc.json              # ESLint rules
│   ├── .env.example                # Environment template
│   └── FRONTEND_SETUP.md           # Frontend documentation
│
└── Documentation
    ├── this file (QUICKSTART.md)
    └── Integration guide
```

## 🚀 Quick Start (5 Minutes)

### Step 1: Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Set environment variables (Windows PowerShell)
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "password"
$env:DB_NAME = "fintech_analytics"

# Start FastAPI server
python main.py
```

The backend will start on `http://localhost:8000`

### Step 2: Frontend Setup

```bash
# Install Node dependencies
npm install

# Start development server
npm run dev
```

The frontend will open automatically on `http://localhost:5173`

### Step 3: Test the Integration

1. Click **"Generate Sample Batch"** button
2. Click **"Run Spark Analytics Engine"** button
3. Wait for processing (shows loading spinner)
4. View results in the dashboard

## 🔧 Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Java 8+** (for PySpark)
- **PostgreSQL 12+** (local or AWS RDS)
- **Git** (optional)

## 📚 Detailed Setup Guides

### Backend

See [DATABASE_SETUP.md](./DATABASE_SETUP.md) for:

- PostgreSQL installation and configuration
- AWS RDS setup guide
- Environment variable configuration
- Troubleshooting

See [README.md](./README.md) for:

- API documentation
- Risk assessment logic
- Performance considerations
- Production deployment

### Frontend

See [FRONTEND_SETUP.md](./FRONTEND_SETUP.md) for:

- Node.js and npm setup
- React component documentation
- Tailwind CSS customization
- Deployment guides

## 🌐 API Endpoints

### POST /api/process-risk

**Process batch of customer applications**

Request:

```json
[
  {
    "applicationId": "APP001",
    "income": 60000,
    "monthlyDebt": 2500,
    "creditScore": 720,
    "applicantName": "John Doe"
  }
]
```

Response:

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
  }
]
```

### GET /api/history

**Retrieve last 50 processed records from database**

Response:

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
  }
]
```

### GET /health

**Health check endpoint**

Response:

```json
{
  "status": "healthy",
  "service": "FinTech Credit Risk Analytics Engine"
}
```

## 🎯 Key Features

### ✅ Backend

- **PySpark DataFrame Processing**: Vectorized batch operations
- **PostgreSQL Persistence**: JDBC writer for automatic data storage
- **FastAPI REST API**: Modern async HTTP server
- **Type Safety**: Pydantic models for validation
- **Environment Configuration**: Flexible deployment options

### ✅ Frontend

- **Interactive Dashboard**: Beautiful dark theme UI
- **Tab Navigation**: Batch Processing → Results → History
- **Batch Simulation**: Generate mock financial profiles
- **Real-time Processing**: Loading indicators and status messages
- **Data Visualization**: Summary cards and color-coded tables
- **Export Functionality**: Download results as JSON
- **History Tracking**: View all processed records

## 📊 Risk Assessment Logic

### Debt-to-Income Ratio (DTI)

```
DTI = monthlyDebt / (income / 12)
```

### Risk Status

- **Rejected**: If `creditScore < 600` OR `DTI > 0.45`
- **Approved**: Otherwise

### Interest Rate

- **Approved**: `0.05 + (0.10 * DTI)` (5% + 10% of DTI)
- **Rejected**: `0.0` (0%)

## 🗄️ Database Schema

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

## 🔒 Security Checklist

- ✅ Environment variables for sensitive data (DB credentials)
- ✅ Type validation with Pydantic
- ✅ Error handling without exposing internals
- ✅ CORS configuration (configure as needed)
- ✅ No hardcoded secrets in codebase
- ✅ HTTPS ready for production

## 📈 Performance Tips

### Backend

1. **Batch Processing**: Send multiple records per request
2. **Connection Pooling**: Configure for production databases
3. **Spark Partitioning**: Optimize for your data size
4. **Caching**: Enable if processing same data repeatedly

### Frontend

1. **Lazy Loading**: Components load on demand
2. **Memoization**: Avoid unnecessary re-renders with React.memo
3. **Image Optimization**: Use modern formats (WebP)
4. **Code Splitting**: Vite automatically handles this

## 🚢 Production Deployment

### Backend (Python)

```bash
# Using Gunicorn + Uvicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# Or using Docker
docker build -t fintech-backend .
docker run -p 8000:8000 fintech-backend
```

### Frontend (React)

```bash
# Build for production
npm run build

# Deploy dist/ folder to:
# - Vercel, Netlify, GitHub Pages
# - AWS S3 + CloudFront
# - Azure Static Web Apps
# - Any static hosting service
```

### Database

- Use AWS RDS PostgreSQL for managed service
- Enable automated backups
- Use VPC for security
- Monitor with CloudWatch

## 🐛 Troubleshooting

### Connection Issues

1. Verify backend is running: `http://localhost:8000/health`
2. Check frontend console for CORS errors
3. Ensure PostgreSQL credentials are correct

### Missing Dependencies

```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### Database Errors

```bash
# Check PostgreSQL is running
psql -U postgres

# Create database if needed
createdb fintech_analytics
```

### Port Already in Use

```bash
# Change backend port in main.py
# Change frontend port in vite.config.js
```

## 📖 Learning Resources

- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev)
- [Tailwind CSS Docs](https://tailwindcss.com)
- [PostgreSQL Guide](https://www.postgresql.org/docs/)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

This project is provided as-is for educational and commercial use.

## 🆘 Support

For issues or questions:

1. **Backend Issues**: See [README.md](./README.md)
2. **Frontend Issues**: See [FRONTEND_SETUP.md](./FRONTEND_SETUP.md)
3. **Database Issues**: See [DATABASE_SETUP.md](./DATABASE_SETUP.md)
4. **Check the troubleshooting sections above**

## 🎉 Next Steps

1. ✅ Complete setup following this guide
2. ✅ Generate sample batches and test processing
3. ✅ Customize risk assessment logic as needed
4. ✅ Configure PostgreSQL for production
5. ✅ Deploy backend and frontend
6. ✅ Monitor performance and logs

---

**Built with**: Python, PySpark, FastAPI, React, Tailwind CSS, PostgreSQL

**Last Updated**: May 27, 2026
