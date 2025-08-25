import streamlit as st
from app.services.database_manager import get_db_manager
import os

def render_database_connection():
    """Render the database connection configuration interface."""
    
    db_manager = get_db_manager()
    
    st.sidebar.header("🔌 Database Connection")
    
    # Show current connection status
    if db_manager.is_connected():
        conn_info = db_manager.get_connection_info()
        st.sidebar.success(f"✅ Connected to {conn_info['type'].upper()}")
        
        # Show connection details
        with st.sidebar.expander("Connection Details"):
            st.write(f"**Type:** {conn_info['type']}")
            if conn_info['type'] == 'sqlite':
                st.write(f"**Path:** {conn_info['parameters'].get('db_path', 'data/sample.db')}")
            else:
                st.write(f"**Host:** {conn_info['parameters'].get('host', 'localhost')}")
                st.write(f"**Port:** {conn_info['parameters'].get('port', '')}")
                st.write(f"**Database:** {conn_info['parameters'].get('database', '')}")
                st.write(f"**Username:** {conn_info['parameters'].get('username', '')}")
        
        # Connection actions
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🔄 Test Connection"):
                if db_manager.test_connection():
                    st.success("✅ Connection is healthy!")
                else:
                    st.error("❌ Connection failed!")
        
        with col2:
            if st.button("🔌 Disconnect"):
                db_manager.disconnect()
                st.sidebar.info("Disconnected from database")
                st.rerun()
    
    else:
        st.sidebar.warning("❌ No database connected")
        
        # Quick connection options
        st.sidebar.subheader("🚀 Quick Connect")
        
        # Default SQLite connection
        if st.sidebar.button("📁 Connect to Default SQLite", type="primary"):
            db_manager = get_db_manager()
            if db_manager.connect("sqlite", db_path="data/sample.db"):
                st.sidebar.success("✅ Connected to default SQLite database!")
                st.rerun()
            else:
                st.sidebar.error("❌ Failed to connect to default database")
    
    # Always show database type selection and connection forms
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔗 Connect to Other Database")
    
    if db_manager.is_connected():
        st.sidebar.info("💡 You can connect to a different database type. This will disconnect your current connection.")
    
    db_type = st.sidebar.selectbox(
        "Select Database Type:",
        ["sqlite", "postgresql", "mysql", "sqlserver", "oracle"],
        help="Choose the type of database you want to connect to"
    )
    
    if db_type == "sqlite":
        render_sqlite_connection()
    elif db_type == "postgresql":
        render_postgresql_connection()
    elif db_type == "mysql":
        render_mysql_connection()
    elif db_type == "sqlserver":
        render_sqlserver_connection()
    elif db_type == "oracle":
        render_oracle_connection()
    
    # Auto-disconnect if user selects different database type than current
    if db_manager.is_connected():
        current_type = db_manager.get_connection_info()['type']
        if current_type != db_type:
            st.sidebar.warning(f"⚠️ You're currently connected to {current_type.upper()}. Select '{current_type}' above to see current connection options, or connect to {db_type.upper()} to switch.")

def render_sqlite_connection():
    """Render SQLite connection form."""
    st.sidebar.subheader("SQLite Connection")
    
    db_path = st.sidebar.text_input(
        "Database Path:",
        value="data/sample.db",
        help="Path to your SQLite database file"
    )
    
    # File browser option
    if st.sidebar.checkbox("Browse for file"):
        uploaded_file = st.sidebar.file_uploader(
            "Choose SQLite database file",
            type=['db', 'sqlite', 'sqlite3'],
            help="Upload your SQLite database file"
        )
        if uploaded_file is not None:
            # Save uploaded file to data directory
            save_path = f"data/{uploaded_file.name}"
            os.makedirs("data", exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            db_path = save_path
            st.sidebar.success(f"File saved to: {save_path}")
    
    if st.sidebar.button("🔗 Connect to SQLite"):
        db_manager = get_db_manager()
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        if db_manager.connect("sqlite", db_path=db_path):
            st.sidebar.success("✅ Connected to SQLite database!")
            st.rerun()
        else:
            st.sidebar.error("❌ Failed to connect to SQLite database")

def render_postgresql_connection():
    """Render PostgreSQL connection form."""
    st.sidebar.subheader("PostgreSQL Connection")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        host = st.text_input("Host:", value="localhost")
        port = st.number_input("Port:", value=5432, min_value=1, max_value=65535)
        database = st.text_input("Database:", value="postgres")
    
    with col2:
        username = st.text_input("Username:", value="postgres")
        password = st.text_input("Password:", type="password")
    
    # Connection options
    col1, col2 = st.sidebar.columns(2)
    with col1:
        use_ssl = st.checkbox("Use SSL", value=False)
    with col2:
        timeout = st.number_input("Timeout (s):", value=10, min_value=1, max_value=60)
    
    if st.sidebar.button("🔗 Connect to PostgreSQL"):
        db_manager = get_db_manager()
        
        connection_params = {
            "host": host,
            "port": port,
            "database": database,
            "username": username,
            "password": password
        }
        
        if db_manager.connect("postgresql", **connection_params):
            st.sidebar.success("✅ Connected to PostgreSQL database!")
            st.rerun()
        else:
            st.sidebar.error("❌ Failed to connect to PostgreSQL database")

def render_mysql_connection():
    """Render MySQL connection form."""
    st.sidebar.subheader("MySQL Connection")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        host = st.text_input("Host:", value="localhost", key="mysql_host")
        port = st.number_input("Port:", value=3306, min_value=1, max_value=65535, key="mysql_port")
        database = st.text_input("Database:", value="mysql", key="mysql_database")
    
    with col2:
        username = st.text_input("Username:", value="root", key="mysql_username")
        password = st.text_input("Password:", type="password", key="mysql_password")
    
    # Connection options
    col1, col2 = st.sidebar.columns(2)
    with col1:
        use_ssl = st.checkbox("Use SSL", value=False, key="mysql_ssl")
    with col2:
        charset = st.selectbox("Charset:", ["utf8mb4", "utf8", "latin1"], key="mysql_charset")
    
    # Debug information
    with st.sidebar.expander("🔍 Debug Info"):
        st.write(f"**Host:** {host}")
        st.write(f"**Port:** {port} (type: {type(port)})")
        st.write(f"**Database:** {database}")
        st.write(f"**Username:** {username}")
        st.write(f"**Password:** {'*' * len(password) if password else 'None'}")
        st.write(f"**Charset:** {charset}")
    
    if st.sidebar.button("🔗 Connect to MySQL", key="mysql_connect"):
        db_manager = get_db_manager()
        
        # Validate inputs
        if not host or not username or not database:
            st.sidebar.error("❌ Please fill in all required fields (Host, Username, Database)")
            return
        
        # Ensure port is a valid integer
        try:
            port_int = int(port)
            if port_int < 1 or port_int > 65535:
                st.sidebar.error("❌ Port must be between 1 and 65535")
                return
        except (ValueError, TypeError):
            st.sidebar.error("❌ Invalid port number")
            return
        
        connection_params = {
            "host": host.strip(),
            "port": port_int,
            "database": database.strip(),
            "username": username.strip(),
            "password": password.strip() if password else "",
            "charset": charset
        }
        
        # Show connection attempt
        st.sidebar.info(f"🔄 Attempting to connect to MySQL at {host}:{port_int}...")
        
        if db_manager.connect("mysql", **connection_params):
            st.sidebar.success("✅ Connected to MySQL database!")
            st.rerun()
        else:
            st.sidebar.error("❌ Failed to connect to MySQL database")
            st.sidebar.info("💡 Check if MySQL server is running and credentials are correct")

def render_sqlserver_connection():
    """Render SQL Server connection form."""
    try:
        st.sidebar.subheader("SQL Server Connection")
        
        # Simplified connection form - always show basic connection
        st.sidebar.markdown("**Connection Settings**")
        
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            host = st.text_input("Server/Instance:", value="localhost", 
                                help="Enter server name or IP address. For named instances, use: SERVER\\INSTANCE")
            port = st.number_input("Port:", value=1433, min_value=1, max_value=65535,
                                  help="Default SQL Server port is 1433")
            database = st.text_input("Database:", value="master",
                                    help="Enter database name or leave as 'master' to connect to server")
        
        with col2:
            username = st.text_input("Username:", value="sa",
                                    help="SQL Server authentication username")
            password = st.text_input("Password:", type="password",
                                    help="SQL Server authentication password")
        
        # Authentication method
        auth_method = st.sidebar.selectbox(
            "Authentication:",
            ["SQL Server Authentication", "Windows Authentication"],
            help="Choose authentication method"
        )
        
        # ODBC Driver selection
        driver = st.sidebar.selectbox(
            "ODBC Driver:",
            [
                "ODBC+Driver+17+for+SQL+Server",
                "ODBC+Driver+18+for+SQL+Server", 
                "ODBC+Driver+13+for+SQL+Server",
                "SQL+Server+Native+Client+11.0"
            ],
            help="Select the ODBC driver installed on your system"
        )
        
        # Connection options
        col1, col2 = st.sidebar.columns(2)
        with col1:
            timeout = st.number_input("Connection Timeout (s):", value=30, min_value=5, max_value=300)
        with col2:
            encrypt = st.checkbox("Encrypt Connection", value=True, 
                                 help="Enable encryption for secure connections")
        
        # Database discovery option
        discover_databases = st.sidebar.checkbox("Discover Available Databases", value=False,
                                               help="Connect to server first, then browse available databases")
        
        # Action buttons
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("🧪 Test Connection", type="secondary"):
                test_sqlserver_connection(host, port, "master", username, password, driver, auth_method, timeout, encrypt)
        
        with col2:
            if st.button("🔗 Connect to SQL Server", type="primary"):
                db_manager = get_db_manager()
                
                # If discovering databases, connect to master first
                target_database = "master" if discover_databases else database
                
                connection_params = {
                    "host": host,
                    "port": port,
                    "database": target_database,
                    "username": username if auth_method == "SQL Server Authentication" else "",
                    "password": password if auth_method == "SQL Server Authentication" else "",
                    "driver": driver,
                    "trusted_connection": auth_method == "Windows Authentication",
                    "timeout": timeout,
                    "encrypt": encrypt
                }
                
                if db_manager.connect("sqlserver", **connection_params):
                    if discover_databases:
                        st.sidebar.success("✅ Connected to SQL Server! Now discovering databases...")
                        show_database_discovery(db_manager, host, port, username, password, driver, auth_method, timeout, encrypt)
                    else:
                        st.sidebar.success("✅ Connected to SQL Server database!")
                        st.rerun()
                else:
                    st.sidebar.error("❌ Failed to connect to SQL Server database")
        
        # Common SQL Server presets
        st.sidebar.markdown("---")
        st.sidebar.subheader("🚀 Quick Connect Presets")
        
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("🏠 Local SQL Server"):
                connect_sqlserver_preset("localhost", 1433, "master", "sa", "", "ODBC+Driver+17+for+SQL+Server")
            
            if st.button("🗄️ SQL Server Express"):
                connect_sqlserver_preset("localhost\\SQLEXPRESS", 1433, "master", "sa", "", "ODBC+Driver+17+for+SQL+Server")
        
        with col2:
            if st.button("☁️ Azure SQL"):
                connect_sqlserver_preset("your-server.database.windows.net", 1433, "your-database", "your-username", "", "ODBC+Driver+17+for+SQL+Server")
            
            if st.button("🐳 Docker SQL Server"):
                connect_sqlserver_preset("localhost", 1433, "master", "sa", "YourStrong@Passw0rd", "ODBC+Driver+17+for+SQL+Server")
                
    except Exception as e:
        st.sidebar.error(f"Error rendering SQL Server connection: {str(e)}")
        st.sidebar.info("Please check the console for more details.")
        # Fallback to simple form
        st.sidebar.text_input("Server:", value="localhost")
        st.sidebar.text_input("Database:", value="master")
        st.sidebar.text_input("Username:", value="sa")
        st.sidebar.text_input("Password:", type="password")
        if st.sidebar.button("Connect"):
            st.sidebar.error("Connection failed. Please check your settings.")

def render_sqlserver_basic_connection():
    """Render basic SQL Server connection form."""
    st.sidebar.markdown("**Basic Connection Settings**")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        host = st.text_input("Server/Instance:", value="localhost", 
                            help="Enter server name or IP address. For named instances, use: SERVER\\INSTANCE")
        port = st.number_input("Port:", value=1433, min_value=1, max_value=65535,
                              help="Default SQL Server port is 1433")
        database = st.text_input("Database:", value="master",
                                help="Enter database name or leave as 'master' to connect to server")
    
    with col2:
        username = st.text_input("Username:", value="sa",
                                help="SQL Server authentication username")
        password = st.text_input("Password:", type="password",
                                help="SQL Server authentication password")
    
    # Authentication method
    auth_method = st.sidebar.selectbox(
        "Authentication:",
        ["SQL Server Authentication", "Windows Authentication"],
        help="Choose authentication method"
    )
    
    # ODBC Driver selection
    driver = st.sidebar.selectbox(
        "ODBC Driver:",
        [
            "ODBC+Driver+17+for+SQL+Server",
            "ODBC+Driver+18+for+SQL+Server", 
            "ODBC+Driver+13+for+SQL+Server",
            "SQL+Server+Native+Client+11.0"
        ],
        help="Select the ODBC driver installed on your system"
    )
    
    # Connection options
    col1, col2 = st.sidebar.columns(2)
    with col1:
        timeout = st.number_input("Connection Timeout (s):", value=30, min_value=5, max_value=300)
    with col2:
        encrypt = st.checkbox("Encrypt Connection", value=True, 
                             help="Enable encryption for secure connections")
    
    # Database discovery option
    discover_databases = st.sidebar.checkbox("Discover Available Databases", value=False,
                                           help="Connect to server first, then browse available databases")
    
    # Action buttons
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🧪 Test Connection", type="secondary"):
            test_sqlserver_connection(host, port, "master", username, password, driver, auth_method, timeout, encrypt)
    
    with col2:
        if st.button("🔗 Connect to SQL Server", type="primary"):
            db_manager = get_db_manager()
            
            # If discovering databases, connect to master first
            target_database = "master" if discover_databases else database
            
            connection_params = {
                "host": host,
                "port": port,
                "database": target_database,
                "username": username if auth_method == "SQL Server Authentication" else "",
                "password": password if auth_method == "SQL Server Authentication" else "",
                "driver": driver,
                "trusted_connection": auth_method == "Windows Authentication",
                "timeout": timeout,
                "encrypt": encrypt
            }
            
            if db_manager.connect("sqlserver", **connection_params):
                if discover_databases:
                    st.sidebar.success("✅ Connected to SQL Server! Now discovering databases...")
                    show_database_discovery(db_manager, host, port, username, password, driver, auth_method, timeout, encrypt)
                else:
                    st.sidebar.success("✅ Connected to SQL Server database!")
                    st.rerun()
            else:
                st.sidebar.error("❌ Failed to connect to SQL Server database")

def render_sqlserver_advanced_connection():
    """Render advanced SQL Server connection form."""
    st.sidebar.markdown("**Advanced Connection Settings**")
    
    # Server details
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        host = st.text_input("Server:", value="localhost")
        instance_name = st.text_input("Instance Name:", value="",
                                     help="Leave empty for default instance")
        port = st.number_input("Port:", value=1433, min_value=1, max_value=65535)
    
    with col2:
        database = st.text_input("Database:", value="master")
        application_name = st.text_input("Application Name:", value="NLP-SQL-Assistant",
                                       help="Name shown in SQL Server activity monitor")
    
    # Authentication details
    st.sidebar.markdown("**Authentication**")
    auth_method = st.sidebar.selectbox(
        "Method:",
        ["SQL Server Authentication", "Windows Authentication", "Azure Active Directory"]
    )
    
    if auth_method == "SQL Server Authentication":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            username = st.text_input("Username:", value="sa")
        with col2:
            password = st.text_input("Password:", type="password")
    elif auth_method == "Azure Active Directory":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            username = st.text_input("Username:", value="your-email@domain.com")
        with col2:
            password = st.text_input("Password:", type="password")
    
    # Connection options
    st.sidebar.markdown("**Connection Options**")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        driver = st.selectbox("ODBC Driver:", [
            "ODBC+Driver+17+for+SQL+Server",
            "ODBC+Driver+18+for+SQL+Server",
            "ODBC+Driver+13+for+SQL+Server"
        ])
        timeout = st.number_input("Connection Timeout (s):", value=30, min_value=5, max_value=300)
    
    with col2:
        encrypt = st.checkbox("Encrypt Connection", value=True)
        trust_cert = st.checkbox("Trust Server Certificate", value=False,
                                help="Trust server certificate for encrypted connections")
    
    # Additional options
    col1, col2 = st.sidebar.columns(2)
    with col1:
        multiple_activeresultsets = st.checkbox("Multiple Active Result Sets", value=False)
        autocommit = st.checkbox("Auto Commit", value=False)
    
    with col2:
        connection_retry_count = st.number_input("Retry Count:", value=1, min_value=0, max_value=10)
        connection_retry_interval = st.number_input("Retry Interval (s):", value=10, min_value=1, max_value=60)
    
    if st.sidebar.button("🔗 Connect with Advanced Settings", type="primary"):
        db_manager = get_db_manager()
        
        # Build server name with instance
        server_name = host
        if instance_name:
            server_name = f"{host}\\{instance_name}"
        
        connection_params = {
            "host": server_name,
            "port": port,
            "database": database,
            "username": username if auth_method != "Windows Authentication" else "",
            "password": password if auth_method != "Windows Authentication" else "",
            "driver": driver,
            "trusted_connection": auth_method == "Windows Authentication",
            "timeout": timeout,
            "encrypt": encrypt,
            "trust_cert": trust_cert,
            "application_name": application_name,
            "multiple_activeresultsets": multiple_activeresultsets,
            "autocommit": autocommit,
            "connection_retry_count": connection_retry_count,
            "connection_retry_interval": connection_retry_interval
        }
        
        if db_manager.connect("sqlserver", **connection_params):
            st.sidebar.success("✅ Connected to SQL Server with advanced settings!")
            st.rerun()
        else:
            st.sidebar.error("❌ Failed to connect to SQL Server database")

def render_sqlserver_connection_string():
    """Render SQL Server connection string form."""
    st.sidebar.markdown("**Connection String Builder**")
    
    # Connection string template
    st.sidebar.markdown("**Connection String Template:**")
    
    # Server
    server = st.sidebar.text_input("Server:", value="localhost",
                                  help="Server name or IP address")
    
    # Database
    database = st.sidebar.text_input("Database:", value="master",
                                    help="Database name")
    
    # Authentication
    auth_type = st.sidebar.selectbox("Authentication Type:", [
        "SQL Server Authentication",
        "Windows Authentication", 
        "Azure Active Directory"
    ])
    
    if auth_type == "SQL Server Authentication":
        username = st.sidebar.text_input("Username:", value="sa")
        password = st.sidebar.text_input("Password:", type="password")
    elif auth_type == "Azure Active Directory":
        username = st.sidebar.text_input("Username:", value="your-email@domain.com")
        password = st.sidebar.text_input("Password:", type="password")
    
    # Driver
    driver = st.sidebar.selectbox("ODBC Driver:", [
        "ODBC+Driver+17+for+SQL+Server",
        "ODBC+Driver+18+for+SQL+Server",
        "ODBC+Driver+13+for+SQL+Server"
    ])
    
    # Options
    col1, col2 = st.sidebar.columns(2)
    with col1:
        encrypt = st.checkbox("Encrypt", value=True)
        trust_cert = st.checkbox("Trust Server Certificate", value=False)
        timeout = st.number_input("Connection Timeout", value=30)
    
    with col2:
        application_name = st.text_input("Application Name", value="NLP-SQL-Assistant")
        multiple_activeresultsets = st.checkbox("MARS", value=False)
    
    # Generate connection string
    connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
    
    if auth_type == "Windows Authentication":
        connection_string += "Trusted_Connection=yes;"
    else:
        connection_string += f"UID={username};PWD={password};"
    
    connection_string += f"Encrypt={'yes' if encrypt else 'no'};"
    if trust_cert:
        connection_string += "TrustServerCertificate=yes;"
    
    connection_string += f"Connection Timeout={timeout};"
    connection_string += f"Application Name={application_name};"
    
    if multiple_activeresultsets:
        connection_string += "MultipleActiveResultSets=true;"
    
    # Display connection string
    st.sidebar.markdown("**Generated Connection String:**")
    st.sidebar.code(connection_string, language="text")
    
    # Copy button
    if st.sidebar.button("📋 Copy Connection String"):
        st.sidebar.success("Connection string copied to clipboard!")
    
    # Connect using connection string
    if st.sidebar.button("🔗 Connect using Connection String", type="primary"):
        db_manager = get_db_manager()
        
        # Parse connection string and connect
        try:
            # For now, we'll use the basic connection method
            # In a full implementation, you'd parse the connection string
            connection_params = {
                "host": server,
                "port": 1433,
                "database": database,
                "username": username if auth_type != "Windows Authentication" else "",
                "password": password if auth_type != "Windows Authentication" else "",
                "driver": driver,
                "trusted_connection": auth_type == "Windows Authentication",
                "encrypt": encrypt,
                "trust_cert": trust_cert,
                "timeout": timeout,
                "application_name": application_name,
                "multiple_activeresultsets": multiple_activeresultsets
            }
            
            if db_manager.connect("sqlserver", **connection_params):
                st.sidebar.success("✅ Connected using connection string!")
                st.rerun()
            else:
                st.sidebar.error("❌ Failed to connect using connection string")
        except Exception as e:
            st.sidebar.error(f"❌ Error: {str(e)}")

def connect_sqlserver_preset(host, port, database, username, password, driver):
    """Connect to SQL Server using preset parameters."""
    db_manager = get_db_manager()
    
    connection_params = {
        "host": host,
        "port": port,
        "database": database,
        "username": username,
        "password": password,
        "driver": driver
    }
    
    if db_manager.connect("sqlserver", **connection_params):
        st.sidebar.success(f"✅ Connected to SQL Server at {host}!")
        st.rerun()
    else:
        st.sidebar.error(f"❌ Failed to connect to SQL Server at {host}")

def render_oracle_connection():
    """Render Oracle connection form."""
    st.sidebar.subheader("Oracle Connection")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        host = st.text_input("Host:", value="localhost")
        port = st.number_input("Port:", value=1521, min_value=1, max_value=65535)
        service_name = st.text_input("Service Name:", value="ORCL")
    
    with col2:
        username = st.text_input("Username:", value="system")
        password = st.text_input("Password:", type="password")
    
    # Connection options
    col1, col2 = st.sidebar.columns(2)
    with col1:
        use_tns = st.checkbox("Use TNS", value=False)
    with col2:
        encoding = st.selectbox("Encoding:", ["UTF-8", "AL32UTF8", "WE8ISO8859P1"])
    
    if st.sidebar.button("🔗 Connect to Oracle"):
        db_manager = get_db_manager()
        
        connection_params = {
            "host": host,
            "port": port,
            "service_name": service_name,
            "username": username,
            "password": password,
            "encoding": encoding
        }
        
        if db_manager.connect("oracle", **connection_params):
            st.sidebar.success("✅ Connected to Oracle database!")
            st.rerun()
        else:
            st.sidebar.error("❌ Failed to connect to Oracle database")

def render_connection_help():
    """Render help information for database connections."""
    with st.sidebar.expander("ℹ️ Connection Help"):
        st.markdown("""
        **SQLite:**
        - Just provide the path to your .db file
        - Example: `data/my_database.db`
        - You can also upload a database file
        
        **PostgreSQL:**
        - Make sure PostgreSQL is running
        - Default port is 5432
        - You may need to enable password authentication
        
        **MySQL:**
        - Make sure MySQL server is running
        - Default port is 3306
        - Root user typically has no password by default
        
        **SQL Server:**
        - Install ODBC Driver for SQL Server
        - Enable TCP/IP protocol in SQL Server Configuration Manager
        - Default port is 1433
        - Can use Windows Authentication
        - For named instances, use: SERVER\\INSTANCE
        
        **Oracle:**
        - Make sure Oracle Database is running
        - Default port is 1521
        - Service name is usually ORCL or XE
        
        **Troubleshooting:**
        - Check if the database server is running
        - Verify credentials and permissions
        - Ensure network connectivity
        - Check firewall settings
        """)
        
        # SQL Server specific help
        with st.expander("🔧 SQL Server Troubleshooting"):
            st.markdown("""
            **Common SQL Server Issues:**
            
            **1. Connection Refused:**
            - Verify SQL Server service is running
            - Check if TCP/IP protocol is enabled
            - Verify port 1433 is not blocked by firewall
            
            **2. Authentication Failed:**
            - Check username/password
            - Verify SQL Server authentication mode
            - For Windows Auth, ensure domain access
            
            **3. ODBC Driver Issues:**
            - Install Microsoft ODBC Driver for SQL Server
            - Download from Microsoft's website
            - Restart application after installation
            
            **4. Named Instance Connection:**
            - Use format: SERVER\\INSTANCE
            - Example: localhost\\SQLEXPRESS
            - Verify instance name in SQL Server Configuration Manager
            
            **5. Encryption Issues:**
            - Enable "Trust Server Certificate" for development
            - Use proper SSL certificates for production
            - Check SQL Server encryption settings
            
            **6. Network Issues:**
            - Verify SQL Server Browser service is running
            - Check SQL Server Configuration Manager
            - Ensure SQL Server is listening on correct port
            """)

def render_connection_presets():
    """Render connection presets for common configurations."""
    with st.sidebar.expander("⚙️ Connection Presets"):
        st.markdown("**Common Configurations:**")
        
        # SQL Server presets
        st.markdown("**🗄️ SQL Server Presets:**")
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("🏠 Local SQL Server"):
                connect_sqlserver_preset("localhost", 1433, "master", "sa", "", "ODBC+Driver+17+for+SQL+Server")
            
            if st.button("🗄️ SQL Server Express"):
                connect_sqlserver_preset("localhost\\SQLEXPRESS", 1433, "master", "sa", "", "ODBC+Driver+17+for+SQL+Server")
        
        with col2:
            if st.button("☁️ Azure SQL"):
                connect_sqlserver_preset("your-server.database.windows.net", 1433, "your-database", "your-username", "", "ODBC+Driver+17+for+SQL+Server")
            
            if st.button("🐳 Docker SQL Server"):
                connect_sqlserver_preset("localhost", 1433, "master", "sa", "YourStrong@Passw0rd", "ODBC+Driver+17+for+SQL+Server")
        
        st.markdown("---")
        
        # Other database presets
        st.markdown("**Other Databases:**")
        
        # PostgreSQL presets
        if st.button("🐘 PostgreSQL (Docker)"):
            db_manager = get_db_manager()
            if db_manager.connect("postgresql", 
                                host="localhost", port=5432, 
                                database="postgres", username="postgres", password="postgres"):
                st.success("✅ Connected to PostgreSQL (Docker)!")
                st.rerun()
        
        # MySQL presets  
        if st.button("🐬 MySQL (Docker)"):
            db_manager = get_db_manager()
            if db_manager.connect("mysql", 
                                host="localhost", port=3306, 
                                database="mysql", username="root", password=""):
                st.success("✅ Connected to MySQL (Docker)!")
                st.rerun()

def initialize_default_connection():
    """Initialize with default SQLite connection if no connection exists."""
    db_manager = get_db_manager()
    
    if not db_manager.is_connected():
        # Try to connect to default SQLite database
        try:
            if db_manager.connect("sqlite", db_path="data/sample.db"):
                st.sidebar.success("✅ Connected to default SQLite database")
        except Exception:
            st.sidebar.warning("⚠️ Could not connect to default database")

def show_database_discovery(db_manager, host, port, username, password, driver, auth_method, timeout, encrypt):
    """Show available databases for selection."""
    try:
        # Get list of available databases
        databases = db_manager.execute_query("SELECT name FROM sys.databases WHERE database_id > 4 ORDER BY name")
        
        if databases:
            st.sidebar.markdown("---")
            st.sidebar.subheader("📚 Available Databases")
            
            # Create a selectbox for database selection
            selected_db = st.sidebar.selectbox(
                "Select Database:",
                [db['name'] for db in databases],
                help="Choose the database you want to work with"
            )
            
            if st.sidebar.button("🔗 Connect to Selected Database"):
                # Reconnect to the selected database
                connection_params = {
                    "host": host,
                    "port": port,
                    "database": selected_db,
                    "username": username if auth_method == "SQL Server Authentication" else "",
                    "password": password if auth_method == "SQL Server Authentication" else "",
                    "driver": driver,
                    "trusted_connection": auth_method == "Windows Authentication",
                    "timeout": timeout,
                    "encrypt": encrypt
                }
                
                if db_manager.connect("sqlserver", **connection_params):
                    st.sidebar.success(f"✅ Connected to database: {selected_db}")
                    st.rerun()
                else:
                    st.sidebar.error(f"❌ Failed to connect to database: {selected_db}")
            
            # Show database information
            with st.sidebar.expander("📊 Database Details"):
                try:
                    db_info = db_manager.execute_query(f"SELECT name, create_date, compatibility_level, recovery_model_desc FROM sys.databases WHERE name = '{selected_db}'")
                    if db_info:
                        info = db_info[0]
                        st.write(f"**Name:** {info['name']}")
                        st.write(f"**Created:** {info['create_date']}")
                        st.write(f"**Compatibility:** {info['compatibility_level']}")
                        st.write(f"**Recovery Model:** {info['recovery_model_desc']}")
                except Exception as e:
                    st.warning(f"Could not retrieve database details: {str(e)}")
        else:
            st.sidebar.warning("No user databases found on this server.")
            
    except Exception as e:
        st.sidebar.error(f"Error discovering databases: {str(e)}")
        st.sidebar.info("You can manually enter the database name above.")

def test_sqlserver_connection(host, port, database, username, password, driver, auth_method, timeout, encrypt):
    """Test SQL Server connection without establishing a full connection."""
    try:
        # Create a temporary connection string for testing
        if auth_method == "Windows Authentication":
            connection_string = f"mssql+pyodbc://@{host}:{port}/{database}?driver={driver}"
        elif password:
            connection_string = f"mssql+pyodbc://{username}:{password}@{host}:{port}/{database}?driver={driver}"
        else:
            connection_string = f"mssql+pyodbc://{username}@{host}:{port}/{database}?driver={driver}"
        
        # Add connection parameters
        params = []
        if timeout:
            params.append(f"timeout={timeout}")
        if encrypt is not None:
            params.append(f"encrypt={'yes' if encrypt else 'no'}")
        
        if params:
            connection_string += "&" + "&".join(params)
        
        # Test the connection
        from sqlalchemy import create_engine, text
        test_engine = create_engine(connection_string, echo=False)
        
        with test_engine.connect() as conn:
            # Test basic connectivity
            result = conn.execute(text("SELECT @@VERSION as version"))
            version = result.fetchone()
            
            # Test server info
            result = conn.execute(text("SELECT @@SERVERNAME as server_name, DB_NAME() as current_db"))
            server_info = result.fetchone()
            
            st.sidebar.success("✅ Connection test successful!")
            
            # Show connection details
            with st.sidebar.expander("📊 Connection Test Results"):
                st.write(f"**Server Version:** {version[0] if version else 'Unknown'}")
                st.write(f"**Server Name:** {server_info[0] if server_info else 'Unknown'}")
                st.write(f"**Current Database:** {server_info[1] if server_info else 'Unknown'}")
                st.write(f"**Connection String:** {connection_string}")
            
            # Clean up test engine
            test_engine.dispose()
            
    except Exception as e:
        st.sidebar.error(f"❌ Connection test failed: {str(e)}")
        
        # Provide helpful error messages
        error_msg = str(e).lower()
        if "timeout" in error_msg:
            st.sidebar.warning("💡 Try increasing the connection timeout or check network connectivity")
        elif "authentication" in error_msg:
            st.sidebar.warning("💡 Check username/password or try Windows Authentication")
        elif "driver" in error_msg:
            st.sidebar.warning("💡 Install Microsoft ODBC Driver for SQL Server")
        elif "encrypt" in error_msg:
            st.sidebar.warning("💡 Try disabling encryption or enable 'Trust Server Certificate'")
        elif "connection refused" in error_msg:
            st.sidebar.warning("💡 Check if SQL Server is running and port is accessible")
