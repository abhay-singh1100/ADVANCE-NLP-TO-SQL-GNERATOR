# Database Connection Guide

This guide explains how to connect to different database types in the Natural Language to SQL Assistant.

## Supported Database Types

### 1. SQLite
- **Use case**: Local development, embedded applications
- **Requirements**: No additional setup needed
- **Connection**: Just provide the path to your .db file

### 2. PostgreSQL
- **Use case**: Production applications, complex queries
- **Requirements**: 
  - PostgreSQL server running
  - `psycopg2-binary` package installed
  - Network access to database server
- **Default port**: 5432

### 3. SQL Server
- **Use case**: Enterprise applications, Windows environments
- **Requirements**:
  - SQL Server instance running
  - ODBC Driver for SQL Server installed
  - `pyodbc` package installed
  - TCP/IP protocol enabled
- **Default port**: 1433

## Installation

Install the required database drivers:

```bash
# For PostgreSQL
pip install psycopg2-binary

# For SQL Server
pip install pyodbc

# Alternative PostgreSQL driver (if psycopg2 fails)
pip install pg8000
```

## Connection Setup

### SQLite Connection
1. Select "SQLite" from the database type dropdown
2. Enter the path to your database file (e.g., `data/my_database.db`)
3. Click "Connect to SQLite"

### PostgreSQL Connection
1. Select "PostgreSQL" from the database type dropdown
2. Fill in the connection details:
   - **Host**: Database server address (default: localhost)
   - **Port**: Database port (default: 5432)
   - **Database**: Database name
   - **Username**: Database username
   - **Password**: Database password
3. Click "Connect to PostgreSQL"

### SQL Server Connection
1. Select "SQL Server" from the database type dropdown
2. Fill in the connection details:
   - **Host**: SQL Server instance address (default: localhost)
   - **Port**: SQL Server port (default: 1433)
   - **Database**: Database name
   - **Username**: SQL Server username
   - **Password**: SQL Server password
   - **ODBC Driver**: Select the appropriate driver version
3. Click "Connect to SQL Server"

## Environment Variables

You can configure database connections using environment variables:

```bash
# PostgreSQL
export DB_HOST=your_postgres_host
export DB_PORT=5432
export DB_NAME=your_database
export DB_USER=your_username
export DB_PASSWORD=your_password

# SQL Server
export SQLSERVER_HOST=your_sqlserver_host
export SQLSERVER_PORT=1433
export SQLSERVER_DB=your_database
export SQLSERVER_USER=your_username
export SQLSERVER_PASSWORD=your_password
```

## Troubleshooting

### Common PostgreSQL Issues
- **Connection refused**: Check if PostgreSQL is running
- **Authentication failed**: Verify username/password
- **Database does not exist**: Create the database first
- **Permission denied**: Check user permissions

### Common SQL Server Issues
- **ODBC Driver not found**: Install Microsoft ODBC Driver for SQL Server
- **TCP/IP not enabled**: Enable TCP/IP in SQL Server Configuration Manager
- **Firewall blocking**: Check Windows Firewall settings
- **Authentication mode**: Ensure SQL Server and Windows Authentication is enabled

### General Connection Issues
- **Network connectivity**: Verify network access to database server
- **Port blocking**: Check if database port is open
- **SSL/TLS**: Some databases require SSL connections
- **Connection pooling**: Adjust pool size if you have many concurrent users

## Security Best Practices

1. **Use strong passwords** for database accounts
2. **Limit database user permissions** to only what's necessary
3. **Use SSL/TLS** for production database connections
4. **Regularly update** database drivers and software
5. **Monitor connection logs** for suspicious activity
6. **Use connection pooling** to manage database connections efficiently

## Performance Tips

1. **Connection pooling**: The app automatically manages connection pools
2. **Query optimization**: Use appropriate indexes on your database tables
3. **Network latency**: Choose database servers close to your application
4. **Resource limits**: Monitor database server resource usage

## Example Connection Strings

### SQLite
```
sqlite:///data/my_database.db
```

### PostgreSQL
```
postgresql://username:password@host:port/database
postgresql://username@host:port/database  # No password
```

### SQL Server
```
mssql+pyodbc://username:password@host:port/database?driver=ODBC+Driver+17+for+SQL+Server
mssql+pyodbc://username@host:port/database?driver=ODBC+Driver+17+for+SQL+Server  # No password
```

## Getting Help

If you encounter connection issues:

1. Check the connection help section in the app sidebar
2. Verify your database server is running and accessible
3. Test the connection using database client tools
4. Check the application logs for detailed error messages
5. Ensure all required packages are installed correctly
