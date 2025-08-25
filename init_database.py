#!/usr/bin/env python3
"""
Database Initialization Script
This script creates and initializes the sample database for the enhanced GUI.
"""

import os
import sqlite3
import sys

def create_sample_database():
    """Create a sample database with test data."""
    print("🚀 Initializing sample database...")
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    db_path = "data/sample.db"
    
    try:
        # Connect to database (creates it if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"✅ Connected to database: {db_path}")
        
        # Create sample tables
        print("📋 Creating sample tables...")
        
        # Sales data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,
                date TEXT,
                product TEXT,
                category TEXT,
                amount REAL,
                region TEXT,
                customer_type TEXT
            )
        """)
        
        # Customer data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                region TEXT,
                customer_type TEXT,
                total_spent REAL,
                join_date TEXT
            )
        """)
        
        # Product data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                price REAL,
                cost REAL,
                stock INTEGER,
                supplier TEXT
            )
        """)
        
        print("✅ Tables created successfully")
        
        # Insert sample data
        print("📊 Inserting sample data...")
        
        # Sample sales data
        sales_data = [
            (1, '2024-01-01', 'Laptop Pro', 'Electronics', 1299.99, 'North', 'Premium'),
            (2, '2024-01-02', 'Wireless Mouse', 'Electronics', 49.99, 'South', 'Standard'),
            (3, '2024-01-03', 'Office Chair', 'Furniture', 299.99, 'East', 'Premium'),
            (4, '2024-01-04', 'Desk Lamp', 'Furniture', 79.99, 'West', 'Standard'),
            (5, '2024-01-05', 'Smartphone', 'Electronics', 899.99, 'North', 'Premium'),
            (6, '2024-01-06', 'Coffee Mug', 'Kitchen', 19.99, 'South', 'Standard'),
            (7, '2024-01-07', 'Gaming Headset', 'Electronics', 199.99, 'East', 'Premium'),
            (8, '2024-01-08', 'Notebook', 'Office', 9.99, 'West', 'Standard'),
            (9, '2024-01-09', 'Monitor', 'Electronics', 399.99, 'North', 'Premium'),
            (10, '2024-01-10', 'Keyboard', 'Electronics', 89.99, 'South', 'Standard')
        ]
        
        cursor.executemany("""
            INSERT OR REPLACE INTO sales (id, date, product, category, amount, region, customer_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sales_data)
        
        # Sample customer data
        customers_data = [
            (1, 'John Smith', 'john@email.com', 'North', 'Premium', 2500.00, '2023-01-15'),
            (2, 'Sarah Johnson', 'sarah@email.com', 'South', 'Standard', 800.00, '2023-03-20'),
            (3, 'Mike Davis', 'mike@email.com', 'East', 'Premium', 1800.00, '2023-02-10'),
            (4, 'Lisa Wilson', 'lisa@email.com', 'West', 'Standard', 600.00, '2023-04-05'),
            (5, 'David Brown', 'david@email.com', 'North', 'Premium', 3200.00, '2023-01-01')
        ]
        
        cursor.executemany("""
            INSERT OR REPLACE INTO customers (id, name, email, region, customer_type, total_spent, join_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, customers_data)
        
        # Sample product data
        products_data = [
            (1, 'Laptop Pro', 'Electronics', 1299.99, 800.00, 50, 'TechCorp'),
            (2, 'Wireless Mouse', 'Electronics', 49.99, 25.00, 200, 'TechCorp'),
            (3, 'Office Chair', 'Furniture', 299.99, 150.00, 30, 'FurnitureCo'),
            (4, 'Desk Lamp', 'Furniture', 79.99, 40.00, 100, 'FurnitureCo'),
            (5, 'Smartphone', 'Electronics', 899.99, 500.00, 75, 'MobileTech'),
            (6, 'Coffee Mug', 'Kitchen', 19.99, 8.00, 500, 'KitchenSupplies'),
            (7, 'Gaming Headset', 'Electronics', 199.99, 100.00, 60, 'GamingGear'),
            (8, 'Notebook', 'Office', 9.99, 3.00, 1000, 'OfficeSupplies'),
            (9, 'Monitor', 'Electronics', 399.99, 200.00, 40, 'TechCorp'),
            (10, 'Keyboard', 'Electronics', 89.99, 45.00, 150, 'TechCorp')
        ]
        
        cursor.executemany("""
            INSERT OR REPLACE INTO products (id, name, category, price, cost, stock, supplier)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, products_data)
        
        # Commit changes
        conn.commit()
        
        print(f"✅ Sample data inserted successfully")
        print(f"📊 Sales: {len(sales_data)} records")
        print(f"👥 Customers: {len(customers_data)} records")
        print(f"📦 Products: {len(products_data)} records")
        
        # Show table structure
        print("\n📋 Database Schema:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"   📊 {table_name}: {len(columns)} columns")
            for col in columns:
                print(f"      - {col[1]} ({col[2]})")
        
        # Close connection
        conn.close()
        
        print(f"\n🎉 Database initialization completed successfully!")
        print(f"💾 Database file: {db_path}")
        print(f"📏 File size: {os.path.getsize(db_path) / 1024:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        return False

def test_database():
    """Test the created database."""
    print("\n🔍 Testing database...")
    
    try:
        conn = sqlite3.connect("data/sample.db")
        cursor = conn.cursor()
        
        # Test queries
        print("📊 Testing sample queries...")
        
        # Count records
        cursor.execute("SELECT COUNT(*) FROM sales")
        sales_count = cursor.fetchone()[0]
        print(f"   Sales records: {sales_count}")
        
        cursor.execute("SELECT COUNT(*) FROM customers")
        customers_count = cursor.fetchone()[0]
        print(f"   Customer records: {customers_count}")
        
        cursor.execute("SELECT COUNT(*) FROM products")
        products_count = cursor.fetchone()[0]
        print(f"   Product records: {products_count}")
        
        # Test aggregation
        cursor.execute("SELECT SUM(amount) FROM sales")
        total_sales = cursor.fetchone()[0]
        print(f"   Total sales: ${total_sales:,.2f}")
        
        cursor.execute("SELECT AVG(price) FROM products")
        avg_price = cursor.fetchone()[0]
        print(f"   Average product price: ${avg_price:.2f}")
        
        # Test grouping
        cursor.execute("""
            SELECT category, COUNT(*) as count, AVG(amount) as avg_amount
            FROM sales 
            GROUP BY category
        """)
        category_stats = cursor.fetchall()
        print(f"   Sales by category:")
        for cat, count, avg_amt in category_stats:
            print(f"      {cat}: {count} sales, avg ${avg_amt:.2f}")
        
        conn.close()
        print("✅ Database test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False

def main():
    """Main function."""
    print("=" * 60)
    print("🚀 Database Initialization Script")
    print("=" * 60)
    
    # Create database
    if create_sample_database():
        # Test database
        test_database()
        
        print("\n" + "=" * 60)
        print("🎯 Next Steps:")
        print("1. Run the enhanced GUI: python run_enhanced_gui.py")
        print("2. Connect to the sample database in the sidebar")
        print("3. Try these example queries:")
        print("   - 'Show total sales by category'")
        print("   - 'What are the top 3 products by price?'")
        print("   - 'Display customer spending by region'")
        print("   - 'Find the most expensive product in each category'")
        print("=" * 60)
    else:
        print("\n❌ Database initialization failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
