from typing import Dict, List
from app.services.database_manager import get_db_manager

class SchemaReader:
    def __init__(self):
        self.db_manager = get_db_manager()
    
    def get_formatted_schema(self) -> str:
        """
        Get the database schema formatted as a string for the LLM prompt.
        
        Returns:
            str: Formatted schema string
        """
        if not self.db_manager.is_connected():
            return "No database connected. Please connect to a database first."
        
        schema_info = self.db_manager.get_schema_info()
        formatted_schema = []
        
        for table_name, columns in schema_info.items():
            column_descriptions = []
            for col in columns:
                col_type = col["type"]
                nullable = "NULL" if col["nullable"] else "NOT NULL"
                pk = "PRIMARY KEY" if col["primary_key"] else ""
                default = f"DEFAULT {col['default']}" if col["default"] is not None else ""
                
                attrs = [attr for attr in [pk, nullable, default] if attr]
                col_desc = f"{col['name']} ({col_type})"
                if attrs:
                    col_desc += f" {' '.join(attrs)}"
                column_descriptions.append(col_desc)
            
            table_desc = f"Table: {table_name}\nColumns:\n" + "\n".join(f"  - {col}" for col in column_descriptions)
            formatted_schema.append(table_desc)
        
        return "\n\n".join(formatted_schema)
    
    def get_schema_summary(self) -> Dict[str, List[str]]:
        """
        Get a simplified schema summary with just table names and column names for the current database.
        
        Returns:
            Dict[str, List[str]]: Dictionary mapping table names to lists of column names
        """
        if not self.db_manager.is_connected():
            return {}
        
        schema_info = self.db_manager.get_schema_info()
        return {
            table_name: [col["name"] for col in columns]
            for table_name, columns in schema_info.items()
        }
    
    def get_all_databases_and_tables(self) -> Dict[str, List[str]]:
        """
        Get a dictionary mapping all database names to their table names, handling SQLite and other databases.
        
        Returns:
            Dict[str, List[str]]: Dictionary mapping database names to lists of table names
        """
        if not self.db_manager.is_connected():
            return {}
        
        conn_info = self.db_manager.get_connection_info()
        db_type = conn_info.get('type', '').lower()

        all_db_tables = {}

        if db_type == 'sqlite':
            # For SQLite, get tables from the current database
            tables_query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
            try:
                results = self.db_manager.execute_query(tables_query)
                # Handle results as either dictionaries or tuples
                tables = []
                if results and isinstance(results[0], dict):
                    tables = [row['name'] for row in results]
                elif results and isinstance(results[0], tuple):
                    tables = [row[0] for row in results]
                db_name = conn_info.get('parameters', {}).get('db_path', 'default_db')
                all_db_tables[db_name] = tables
            except Exception as e:
                raise Exception(f"Error executing query: {str(e)}")
        else:
            # For MySQL or other INFORMATION_SCHEMA-supporting databases
            databases_query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys');"
            try:
                databases = [row['SCHEMA_NAME'] for row in self.db_manager.execute_query(databases_query)]
                
                for db in databases:
                    tables_query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s;"
                    tables = [row['TABLE_NAME'] for row in self.db_manager.execute_query(tables_query, params=(db,))]
                    all_db_tables[db] = tables
            except Exception as e:
                raise Exception(f"Error executing query: {str(e)}")
        
        return all_db_tables