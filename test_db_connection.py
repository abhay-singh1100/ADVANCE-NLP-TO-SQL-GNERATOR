#!/usr/bin/env python3
"""
Database Connection Test Script
This script tests the database connection functionality to help troubleshoot issues.
"""

import os
import sys
import sqlite3

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_sqlite_connection():
    """Test basic SQLite connection."""
    print("🔍 Testing SQLite connection...")
    
    # Check if sample database exists
    db_path = "data/sample.db"
    if os.path.exists(db_path):
        print(f"✅ Sample database found at: {db_path}")
        
        try:
            # Test SQLite connection
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get table list
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print(f"✅ Successfully connected to SQLite database")
            print(f"📋 Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table[0]}")
            
            # Test a simple query
            if tables:
                table_name = tables[0][0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"📊 Table '{table_name}' has {count} rows")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ SQLite connection failed: {str(e)}")
            return False
    else:
        print(f"❌ Sample database not found at: {db_path}")
        print("💡 Creating a sample database...")
        
        try:
            # Create data directory
            os.makedirs("data", exist_ok=True)
            
            # Create sample database with test data
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create sample table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sample_data (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    value REAL,
                    category TEXT
                )
            """)
            
            # Insert sample data
            sample_data = [
                (1, "Item A", 100.5, "Category 1"),
                (2, "Item B", 200.3, "Category 1"),
                (3, "Item C", 150.7, "Category 2"),
                (4, "Item D", 300.2, "Category 2"),
                (5, "Item E", 250.1, "Category 1")
            ]
            
            cursor.executemany("INSERT INTO sample_data (id, name, value, category) VALUES (?, ?, ?, ?)", sample_data)
            conn.commit()
            
            print("✅ Sample database created successfully!")
            print(f"📊 Added {len(sample_data)} sample records")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Failed to create sample database: {str(e)}")
            return False

def test_database_manager():
    """Test the database manager service."""
    print("\n🔍 Testing Database Manager service...")
    
    try:
        from app.services.database_manager import get_db_manager
        
        db_manager = get_db_manager()
        print("✅ Database manager imported successfully")
        
        # Test connection
        if db_manager.connect("sqlite", db_path="data/sample.db"):
            print("✅ Database manager connected successfully")
            
            # Test schema reading
            try:
                schema_info = db_manager.get_schema_info()
                print(f"📋 Schema info retrieved: {len(schema_info)} tables")
                
                for table_name, columns in schema_info.items():
                    print(f"   📊 Table: {table_name} ({len(columns)} columns)")
                    for col in columns[:3]:  # Show first 3 columns
                        print(f"      - {col['name']}: {col['type']}")
                    if len(columns) > 3:
                        print(f"      ... and {len(columns) - 3} more columns")
                
            except Exception as e:
                print(f"⚠️ Schema reading failed: {str(e)}")
            
            # Test query execution
            try:
                results = db_manager.execute_query("SELECT COUNT(*) as count FROM sample_data")
                if results:
                    print(f"✅ Query execution successful: {results[0]['count']} records")
                else:
                    print("⚠️ Query returned no results")
            except Exception as e:
                print(f"❌ Query execution failed: {str(e)}")
            
            # Disconnect
            db_manager.disconnect()
            print("✅ Database manager disconnected successfully")
            
        else:
            print("❌ Database manager connection failed")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import database manager: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Database manager test failed: {str(e)}")
        return False
    
    return True

def test_schema_reader():
    """Test the schema reader service."""
    print("\n🔍 Testing Schema Reader service...")
    
    try:
        from app.services.schema_reader import SchemaReader
        
        schema_reader = SchemaReader()
        print("✅ Schema reader imported successfully")
        
        # Test schema summary
        try:
            schema_summary = schema_reader.get_schema_summary()
            print(f"📋 Schema summary retrieved: {len(schema_summary)} tables")
            
            for table_name, columns in schema_summary.items():
                print(f"   📊 Table: {table_name} ({len(columns)} columns)")
                
        except Exception as e:
            print(f"❌ Schema reading failed: {str(e)}")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import schema reader: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Schema reader test failed: {str(e)}")
        return False
    
    return True

def main():
    """Main test function."""
    print("=" * 60)
    print("🚀 Database Connection Test Suite")
    print("=" * 60)
    
    # Test 1: Basic SQLite connection
    sqlite_ok = test_sqlite_connection()
    
    # Test 2: Database Manager service
    manager_ok = test_database_manager()
    
    # Test 3: Schema Reader service
    schema_ok = test_schema_reader()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    print(f"🔌 SQLite Connection: {'✅ PASS' if sqlite_ok else '❌ FAIL'}")
    print(f"🗄️ Database Manager: {'✅ PASS' if manager_ok else '❌ FAIL'}")
    print(f"📋 Schema Reader: {'✅ PASS' if schema_ok else '❌ FAIL'}")
    
    if all([sqlite_ok, manager_ok, schema_ok]):
        print("\n🎉 All tests passed! Database connection should work in the GUI.")
        print("💡 You can now run the enhanced GUI with:")
        print("   python run_enhanced_gui.py")
    else:
        print("\n⚠️ Some tests failed. Please check the error messages above.")
        print("💡 Common issues:")
        print("   - Missing dependencies (run: pip install -r requirements.txt)")
        print("   - Incorrect file paths")
        print("   - Permission issues")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
