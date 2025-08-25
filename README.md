# 🤖 Natural Language to SQL Assistant

A powerful AI-powered application that converts natural language questions into SQL queries and executes them on various database types. Built with Streamlit, Mistral-7B, and SQLAlchemy.

## ✨ Features

- **Natural Language to SQL**: Ask questions in plain English and get SQL queries
- **Multi-Database Support**: Connect to SQLite, PostgreSQL, MySQL, SQL Server, and Oracle
- **Voice Commands**: Use voice input for hands-free operation
- **Schema Detection**: Automatically detects and displays database structure
- **Query Visualization**: Results displayed as tables and charts
- **Connection Management**: Easy database connection with presets and validation
- **Security**: SQL injection prevention and connection pooling

## 🗄️ Supported Databases

| Database | Type | Default Port | Driver |
|----------|------|--------------|---------|
| **SQLite** | Local file | - | Built-in |
| **PostgreSQL** | Server | 5432 | psycopg2-binary |
| **MySQL** | Server | 3306 | pymysql |
| **SQL Server** | Server | 1433 | pyodbc |
| **Oracle** | Server | 1521 | cx-oracle |

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd nlp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run gui/streamlit_app.py
```

### 3. Connect to Database

The app will automatically connect to a default SQLite database. To connect to other databases:

1. **Use the sidebar** to select your database type
2. **Fill in connection details** (host, port, username, password)
3. **Click connect** to establish the connection
4. **Use connection presets** for common configurations

## 🔌 Database Connection Guide

### SQLite (Default)
- No setup required
- Automatically connects to `data/sample.db`
- Upload custom `.db` files through the interface

### PostgreSQL
```bash
# Install driver
pip install psycopg2-binary

# Connection parameters
Host: localhost
Port: 5432
Database: your_database
Username: your_username
Password: your_password
```

### MySQL
```bash
# Install driver
pip install pymysql

# Connection parameters
Host: localhost
Port: 3306
Database: your_database
Username: root
Password: your_password
```

### SQL Server
```bash
# Install driver
pip install pyodbc

# Install ODBC Driver for SQL Server from Microsoft
# Connection parameters
Host: localhost
Port: 1433
Database: master
Username: sa
Password: your_password
```

### Oracle
```bash
# Install driver
pip install cx-oracle

# Connection parameters
Host: localhost
Port: 1521
Service Name: ORCL
Username: system
Password: your_password
```

## 🎯 Usage Examples

### Natural Language Questions
- "Show me total sales by city"
- "What are the top 3 products by revenue?"
- "How many orders were placed last month?"
- "Which customers have the highest purchase amounts?"

### Voice Commands
- Click the microphone button 🎤
- Speak your question clearly
- The app will convert speech to text and process your query

## 🛠️ Advanced Features

### Connection Presets
- **PostgreSQL (Docker)**: Quick connect to Docker containers
- **MySQL (Docker)**: Standard MySQL Docker setup
- **SQL Server Express**: Local SQL Server instance

### Connection Management
- **Test Connection**: Verify database connectivity
- **Connection Details**: View current connection information
- **Disconnect**: Safely close database connections
- **Auto-reconnect**: Automatic reconnection on failure

### Security Features
- **SQL Injection Prevention**: Blocks dangerous operations
- **Connection Pooling**: Efficient resource management
- **Parameterized Queries**: Safe query execution
- **Access Control**: User permission validation

## 📁 Project Structure

```
nlp/
├── app/
│   ├── services/
│   │   ├── database_manager.py    # Multi-database connection manager
│   │   ├── schema_reader.py       # Database schema detection
│   │   ├── sql_generator.py       # Natural language to SQL conversion
│   │   └── voice_service.py       # Speech recognition
│   └── models/
│       └── mistral_model.py       # LLM integration
├── gui/
│   ├── streamlit_app.py           # Main Streamlit application
│   └── database_connection.py     # Database connection interface
├── config/
│   └── database_config.py         # Database configuration
├── data/                          # Sample database and data files
├── docs/                          # Documentation
└── scripts/                       # Utility scripts
```

## 🔧 Configuration

### Environment Variables
```bash
# Database connections
DB_HOST=your_database_host
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password

# Application settings
ENVIRONMENT=development
```

### Custom Database Settings
Edit `config/database_config.py` to add custom connection presets and validation rules.

## 🧪 Testing

### Test Database Connections
```bash
python scripts/test_database_connections.py
```

### Test Individual Components
```bash
# Test database manager
python -c "from app.services.database_manager import get_db_manager; print('Database manager loaded successfully')"

# Test schema reader
python -c "from app.services.schema_reader import SchemaReader; print('Schema reader loaded successfully')"
```

## 🚨 Troubleshooting

### Common Issues

#### Connection Failed
- Verify database server is running
- Check network connectivity
- Validate credentials and permissions
- Ensure correct port numbers

#### Driver Not Found
```bash
# Install missing drivers
pip install psycopg2-binary  # PostgreSQL
pip install pymysql          # MySQL
pip install pyodbc           # SQL Server
pip install cx-oracle        # Oracle
```

#### Permission Denied
- Check user permissions on database
- Verify firewall settings
- Ensure SSL/TLS configuration

### Getting Help
1. Check the connection help section in the app sidebar
2. Review the database connection guide in `docs/DATABASE_CONNECTION.md`
3. Check application logs for detailed error messages
4. Verify all required packages are installed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Streamlit** for the web application framework
- **Mistral AI** for the open-source language model
- **SQLAlchemy** for database abstraction
- **OpenAI Whisper** for speech recognition

## 📞 Support

For questions and support:
- Check the documentation in the `docs/` folder
- Review the troubleshooting section
- Open an issue on GitHub

---

**Built with ❤️ using modern AI and database technologies** 