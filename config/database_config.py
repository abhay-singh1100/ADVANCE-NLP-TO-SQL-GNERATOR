"""
Database configuration and connection presets.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection presets
DATABASE_PRESETS = {
    "sqlite": {
        "default": {
            "db_path": "data/sample.db"
        }
    },
    "postgresql": {
        "default": {
            "host": "localhost",
            "port": 5432,
            "database": "postgres",
            "username": "postgres",
            "password": ""
        },
        "docker": {
            "host": "localhost",
            "port": 5432,
            "database": "postgres",
            "username": "postgres",
            "password": "postgres"
        }
    },
    "sqlserver": {
        "default": {
            "host": "localhost",
            "port": 1433,
            "database": "master",
            "username": "sa",
            "password": "",
            "driver": "ODBC+Driver+17+for+SQL+Server"
        },
        "express": {
            "host": "localhost",
            "port": 1433,
            "database": "master",
            "username": "sa",
            "password": "",
            "driver": "ODBC+Driver+17+for+SQL+Server"
        }
    }
}

# Environment-specific configurations
def get_database_config() -> Dict[str, Any]:
    """Get database configuration based on environment."""
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        # Production database settings
        return {
            "postgresql": {
                "host": os.getenv("DB_HOST", "localhost"),
                "port": int(os.getenv("DB_PORT", "5432")),
                "database": os.getenv("DB_NAME", "postgres"),
                "username": os.getenv("DB_USER", "postgres"),
                "password": os.getenv("DB_PASSWORD", "")
            }
        }
    else:
        # Development database settings
        return DATABASE_PRESETS

# Connection validation rules
CONNECTION_VALIDATION = {
    "sqlite": {
        "required_fields": ["db_path"],
        "optional_fields": []
    },
    "postgresql": {
        "required_fields": ["host", "port", "database", "username"],
        "optional_fields": ["password", "ssl_mode"]
    },
    "sqlserver": {
        "required_fields": ["host", "port", "database", "username"],
        "optional_fields": ["password", "driver", "trusted_connection"]
    }
}

# Default connection timeout and pool settings
DEFAULT_CONNECTION_SETTINGS = {
    "pool_size": 5,
    "max_overflow": 10,
    "pool_timeout": 30,
    "pool_recycle": 1800,  # 30 minutes
    "connect_timeout": 10
}

# SQL injection prevention patterns
DANGEROUS_SQL_PATTERNS = [
    "DROP DATABASE",
    "DROP TABLE", 
    "TRUNCATE",
    "DELETE FROM",
    "UPDATE",
    "INSERT INTO",
    "CREATE TABLE",
    "ALTER TABLE",
    "EXEC",
    "EXECUTE",
    "xp_",
    "sp_"
]
