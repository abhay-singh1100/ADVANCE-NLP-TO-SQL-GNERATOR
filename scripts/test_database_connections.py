#!/usr/bin/env python3
"""
Test script for database connections.
This script tests the connection to different database types.
"""

import sys
import os
import asyncio

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.database_manager import get_db_manager

def test_sqlite_connection():
    """Test SQLite connection."""
    print("🔍 Testing SQLite connection...")
    
    db_manager = get_db_manager()
    
    try:
        # Test connection to default SQLite database
        if db_manager.connect("sqlite", db_path="data/sample.db"):
            print("✅ SQLite connection successful!")
            
            # Test schema reading
            schema = db_manager.get_schema_info()
            print(f"📊 Found {len(schema)} tables in SQLite database")
            
            # Test query execution
            results = db_manager.execute_query("SELECT COUNT(*) as count FROM sales")
            print(f"📈 Query result: {results}")
            
            db_manager.disconnect()
            return True
        else:
            print("❌ SQLite connection failed!")
            return False
            
    except Exception as e:
        print(f"❌ SQLite test error: {str(e)}")
        return False

def test_postgresql_connection():
    """Test PostgreSQL connection."""
    print("\n🔍 Testing PostgreSQL connection...")
    
    db_manager = get_db_manager()
    
    try:
        # Test connection to PostgreSQL (using default settings)
        if db_manager.connect("postgresql", 
                            host="localhost", 
                            port=5432, 
                            database="postgres", 
                            username="postgres", 
                            password=""):
            print("✅ PostgreSQL connection successful!")
            
            # Test basic operations
            schema = db_manager.get_schema_info()
            print(f"📊 Found {len(schema)} tables in PostgreSQL database")
            
            db_manager.disconnect()
            return True
        else:
            print("❌ PostgreSQL connection failed! (This is expected if PostgreSQL is not running)")
            return False
            
    except Exception as e:
        print(f"❌ PostgreSQL test error: {str(e)}")
        return False

def test_sqlserver_connection():
    """Test SQL Server connection."""
    print("\n🔍 Testing SQL Server connection...")
    
    db_manager = get_db_manager()
    
    try:
        # Test connection to SQL Server (using default settings)
        if db_manager.connect("sqlserver", 
                            host="localhost", 
                            port=1433, 
                            database="master", 
                            username="sa", 
                            password="",
                            driver="ODBC+Driver+17+for+SQL+Server"):
            print("✅ SQL Server connection successful!")
            
            # Test basic operations
            schema = db_manager.get_schema_info()
            print(f"📊 Found {len(schema)} tables in SQL Server database")
            
            db_manager.disconnect()
            return True
        else:
            print("❌ SQL Server connection failed! (This is expected if SQL Server is not running)")
            return False
            
    except Exception as e:
        print(f"❌ SQL Server test error: {str(e)}")
        return False

def test_connection_manager():
    """Test the database connection manager functionality."""
    print("\n🔍 Testing Database Connection Manager...")
    
    db_manager = get_db_manager()
    
    try:
        # Test connection state
        print(f"📊 Initial connection state: {db_manager.is_connected()}")
        
        # Test SQLite connection
        if db_manager.connect("sqlite", db_path="data/sample.db"):
            print(f"📊 After SQLite connection: {db_manager.is_connected()}")
            
            # Test connection info
            conn_info = db_manager.get_connection_info()
            print(f"📊 Connection info: {conn_info['type']}")
            
            # Test connection test
            if db_manager.test_connection():
                print("✅ Connection test successful!")
            else:
                print("❌ Connection test failed!")
            
            # Test disconnect
            db_manager.disconnect()
            print(f"📊 After disconnect: {db_manager.is_connected()}")
            
            return True
        else:
            print("❌ Could not establish test connection!")
            return False
            
    except Exception as e:
        print(f"❌ Connection manager test error: {str(e)}")
        return False

def main():
    """Main test function."""
    print("🚀 Starting Database Connection Tests...\n")
    
    results = []
    
    # Test SQLite (should work)
    results.append(("SQLite", test_sqlite_connection()))
    
    # Test PostgreSQL (may not work if not installed)
    results.append(("PostgreSQL", test_postgresql_connection()))
    
    # Test SQL Server (may not work if not installed)
    results.append(("SQL Server", test_sqlserver_connection()))
    
    # Test connection manager
    results.append(("Connection Manager", test_connection_manager()))
    
    # Print summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print("="*50)
    
    # Overall result
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    if passed == total:
        print("🎉 All tests passed!")
    elif passed > 0:
        print(f"⚠️  {passed}/{total} tests passed")
    else:
        print("❌ All tests failed!")
    
    print("\n💡 Note: PostgreSQL and SQL Server tests may fail if the databases are not running.")
    print("   This is normal and expected in development environments.")

if __name__ == "__main__":
    main()
