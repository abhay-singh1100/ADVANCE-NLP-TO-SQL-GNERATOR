from sqlalchemy import create_engine, MetaData, inspect, text, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Dict, List, Optional, Any, Union
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections for different database types."""
    
    def __init__(self):
        self.current_engine = None
        self.current_session = None
        self.current_base = None
        self.connection_info = {}
        
    def get_connection_string(self, db_type: str, **kwargs) -> str:
        """
        Generate connection string for different database types.
        
        Args:
            db_type (str): Type of database ('sqlite', 'postgresql', 'mysql', 'sqlserver', 'oracle')
            **kwargs: Connection parameters
            
        Returns:
            str: SQLAlchemy connection string
        """
        if db_type.lower() == 'sqlite':
            db_path = kwargs.get('db_path', 'data/sample.db')
            return f"sqlite:///{db_path}"
            
        elif db_type.lower() == 'postgresql':
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', 5432)
            database = kwargs.get('database', 'postgres')
            username = kwargs.get('username', 'postgres')
            password = kwargs.get('password', '')
            
            if password:
                return f"postgresql://{username}:{password}@{host}:{port}/{database}"
            else:
                return f"postgresql://{username}@{host}:{port}/{database}"
                
        elif db_type.lower() == 'mysql':
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', 3306)
            database = kwargs.get('database', 'mysql')
            username = kwargs.get('username', 'root')
            password = kwargs.get('password', '')
            charset = kwargs.get('charset', 'utf8mb4')
            
            # Debug logging
            logger.info(f"MySQL connection parameters: host={host}, port={port} (type: {type(port)}), database={database}, username={username}, charset={charset}")
            
            # Ensure port is valid
            try:
                port_int = int(port)
                if port_int < 1 or port_int > 65535:
                    logger.error(f"Invalid MySQL port: {port_int}")
                    raise ValueError(f"Invalid MySQL port: {port_int}")
            except (ValueError, TypeError) as e:
                logger.error(f"MySQL port conversion error: {port} -> {e}")
                raise ValueError(f"Invalid MySQL port: {port}")
            
            if password:
                connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port_int}/{database}?charset={charset}"
            else:
                connection_string = f"mysql+pymysql://{username}@{host}:{port_int}/{database}?charset={charset}"
            
            logger.info(f"Generated MySQL connection string: {connection_string}")
            return connection_string
                
        elif db_type.lower() == 'sqlserver':
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', 1433)
            database = kwargs.get('database', 'master')
            username = kwargs.get('username', 'sa')
            password = kwargs.get('password', '')
            driver = kwargs.get('driver', 'ODBC+Driver+17+for+SQL+Server')
            trusted_connection = kwargs.get('trusted_connection', False)
            timeout = kwargs.get('timeout', 30)
            encrypt = kwargs.get('encrypt', True)
            trust_cert = kwargs.get('trust_cert', False)
            application_name = kwargs.get('application_name', 'NLP-SQL-Assistant')
            multiple_activeresultsets = kwargs.get('multiple_activeresultsets', False)
            autocommit = kwargs.get('autocommit', False)
            connection_retry_count = kwargs.get('connection_retry_count', 1)
            connection_retry_interval = kwargs.get('connection_retry_interval', 10)
            
            # Build connection string with advanced options
            if trusted_connection:
                connection_string = f"mssql+pyodbc://@{host}:{port}/{database}?driver={driver}"
            elif password:
                connection_string = f"mssql+pyodbc://{username}:{password}@{host}:{port}/{database}?driver={driver}"
            else:
                connection_string = f"mssql+pyodbc://{username}@{host}:{port}/{database}?driver={driver}"
            
            # Add advanced connection parameters
            params = []
            if timeout:
                params.append(f"timeout={timeout}")
            if encrypt is not None:
                params.append(f"encrypt={'yes' if encrypt else 'no'}")
            if trust_cert:
                params.append("trustservercertificate=yes")
            if application_name:
                params.append(f"app={application_name}")
            if multiple_activeresultsets:
                params.append("multipleactiveresultsets=true")
            if autocommit:
                params.append("autocommit=true")
            if connection_retry_count > 1:
                params.append(f"connection_retry_count={connection_retry_count}")
            if connection_retry_interval > 1:
                params.append(f"connection_retry_interval={connection_retry_interval}")
            
            if params:
                connection_string += "&" + "&".join(params)
            
            return connection_string
                
        elif db_type.lower() == 'oracle':
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', 1521)
            service_name = kwargs.get('service_name', 'ORCL')
            username = kwargs.get('username', 'system')
            password = kwargs.get('password', '')
            encoding = kwargs.get('encoding', 'UTF-8')
            
            if password:
                return f"oracle+cx_oracle://{username}:{password}@{host}:{port}/?service_name={service_name}&encoding={encoding}"
            else:
                return f"oracle+cx_oracle://{username}@{host}:{port}/?service_name={service_name}&encoding={encoding}"
                
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    
    def connect(self, db_type: str, **kwargs) -> bool:
        """
        Connect to a database with the specified parameters.
        
        Args:
            db_type (str): Type of database
            **kwargs: Connection parameters
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Close existing connection if any
            if self.current_engine:
                self.current_engine.dispose()
            
            # Generate connection string
            connection_string = self.get_connection_string(db_type, **kwargs)
            logger.info(f"Attempting to connect with: {connection_string}")
            
            # Create engine with appropriate settings
            if db_type.lower() == 'sqlite':
                self.current_engine = create_engine(
                    connection_string,
                    pool_size=5,
                    max_overflow=10,
                    pool_timeout=30,
                    pool_recycle=1800,
                    connect_args={"check_same_thread": False}
                )
            else:
                # Common settings for other database types
                engine_kwargs = {
                    "pool_size": 5,
                    "max_overflow": 10,
                    "pool_timeout": 30,
                    "pool_recycle": 1800
                }
                
                # Add database-specific settings
                if db_type.lower() == 'mysql':
                    engine_kwargs["connect_args"] = {
                        "charset": kwargs.get('charset', 'utf8mb4'),
                        "autocommit": False
                    }
                elif db_type.lower() == 'oracle':
                    engine_kwargs["connect_args"] = {
                        "encoding": kwargs.get('encoding', 'UTF-8'),
                        "nencoding": kwargs.get('encoding', 'UTF-8')
                    }
                
                self.current_engine = create_engine(connection_string, **engine_kwargs)
            
            # Test connection
            with self.current_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            # Create session and base
            self.current_session = sessionmaker(autocommit=False, autoflush=False, bind=self.current_engine)
            self.current_base = declarative_base()
            
            # Store connection info
            self.connection_info = {
                'type': db_type,
                'parameters': kwargs,
                'connection_string': connection_string
            }
            
            logger.info(f"Successfully connected to {db_type} database")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to {db_type} database: {str(e)}")
            self.current_engine = None
            self.current_session = None
            self.current_base = None
            self.connection_info = {}
            return False
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Get current connection information."""
        return self.connection_info.copy()
    
    def is_connected(self) -> bool:
        """Check if currently connected to a database."""
        return self.current_engine is not None
    
    def get_engine(self):
        """Get current database engine."""
        if not self.is_connected():
            raise RuntimeError("Not connected to any database")
        return self.current_engine
    
    def get_session(self):
        """Get current database session."""
        if not self.is_connected():
            raise RuntimeError("Not connected to any database")
        return self.current_session
    
    def get_base(self):
        """Get current declarative base."""
        if not self.is_connected():
            raise RuntimeError("Not connected to any database")
        return self.current_base
    
    def test_connection(self) -> bool:
        """Test if current connection is still valid."""
        if not self.is_connected():
            return False
        
        try:
            with self.current_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
    
    def get_schema_info(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get database schema information including tables and columns.
        
        Returns:
            Dict: Schema information
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to any database")
        
        inspector = inspect(self.current_engine)
        schema_info = {}
        
        for table_name in inspector.get_table_names():
            columns = []
            for column in inspector.get_columns(table_name):
                column_info = {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                    "default": str(column["default"]) if column["default"] is not None else None,
                    "primary_key": column.get("primary_key", False)
                }
                columns.append(column_info)
            schema_info[table_name] = columns
        
        return schema_info
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """
        Execute a SQL query and return results.
        
        Args:
            query (str): SQL query to execute
            params (Optional[Dict]): Query parameters
            
        Returns:
            List[Dict]: Query results
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to any database")
        
        # Basic SQL injection prevention
        dangerous_operations = [
            "DROP DATABASE", "DROP TABLE", "TRUNCATE", "DELETE FROM",
            "UPDATE", "INSERT INTO", "CREATE TABLE", "ALTER TABLE"
        ]
        
        query_upper = query.upper()
        if any(op in query_upper for op in dangerous_operations):
            raise ValueError("Query contains dangerous operations that are not allowed")
        
        try:
            with self.current_engine.connect() as connection:
                result = connection.execute(text(query), params or {})
                return [dict(row._mapping) for row in result]
        except Exception as e:
            raise RuntimeError(f"Error executing query: {str(e)}")
    
    def disconnect(self):
        """Disconnect from current database."""
        if self.current_engine:
            self.current_engine.dispose()
            self.current_engine = None
            self.current_session = None
            self.current_base = None
            self.connection_info = {}
            logger.info("Disconnected from database")

# Global database manager instance
db_manager = DatabaseManager()

def get_db_manager() -> DatabaseManager:
    """Get the global database manager instance."""
    return db_manager
