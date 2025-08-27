   # Natural Language to SQL Assistant
# Technical Report

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Overview](#project-overview)
3. [Technical Architecture](#technical-architecture)
4. [Core Components](#core-components)
5. [Implementation Details](#implementation-details)
6. [System Flow](#system-flow)
7. [Installation and Configuration](#installation-and-configuration)
8. [Advanced Features](#advanced-features)
9. [Future Development](#future-development)
10. [Troubleshooting and FAQ](#troubleshooting-and-faq)

## Executive Summary

The Natural Language to SQL Assistant is an innovative application that bridges the gap between natural human language and structured database queries. By leveraging advanced natural language processing (NLP) and machine learning techniques, the system allows users to interact with databases using plain English questions, which are automatically converted into SQL queries. The application supports multiple database types, offers voice command capabilities, and provides rich data visualization features.

This technical report provides a comprehensive overview of the project's architecture, components, implementation details, and features. It serves as both documentation for the current state of the project and a roadmap for future development.

## Project Overview

### Purpose and Goals

The primary purpose of the Natural Language to SQL Assistant is to democratize access to database information by removing the technical barrier of SQL knowledge. The project aims to:

1. **Simplify Data Access**: Enable non-technical users to query databases without SQL knowledge
2. **Enhance Productivity**: Reduce the time required to formulate complex SQL queries
3. **Improve Accessibility**: Provide voice-based interaction for hands-free operation
4. **Support Multiple Databases**: Work seamlessly with various database management systems
5. **Visualize Results**: Present query results in intuitive tables and charts

### Key Features

- **Natural Language Processing**: Convert English questions to SQL queries
- **Multi-Database Support**: Connect to SQLite, PostgreSQL, MySQL, SQL Server, and Oracle
- **Voice Command Interface**: Use speech recognition for hands-free operation
- **Automatic Schema Detection**: Analyze and display database structure
- **Interactive Data Visualization**: Display results as tables and various chart types
- **Advanced Data Analysis**: Statistical summaries, correlation analysis, and data quality assessment
- **Connection Management**: Easy database connection with presets and validation
- **Security Features**: SQL injection prevention and secure connection handling

### Target Users

1. **Business Analysts**: Who need quick insights from databases without writing SQL
2. **Data Scientists**: Who want to explore data rapidly before detailed analysis
3. **Database Administrators**: Who need to perform quick checks or demonstrations
4. **Non-Technical Stakeholders**: Who need data access without technical knowledge
5. **Developers**: Who want to prototype database queries quickly

### Use Cases

1. **Business Intelligence**: Analyzing sales data, customer behavior, and market trends
2. **Data Exploration**: Quickly understanding new datasets and their relationships
3. **Report Generation**: Creating data summaries and visualizations for presentations
4. **Database Administration**: Performing routine checks and simple maintenance tasks
5. **Educational Purposes**: Teaching database concepts without requiring SQL syntax knowledge

### Project Scope

The Natural Language to SQL Assistant currently focuses on:

- **Read Operations**: SELECT queries for data retrieval and analysis
- **Basic Data Manipulation**: Simple filtering, grouping, and aggregation
- **Schema Exploration**: Understanding database structure and relationships
- **Data Visualization**: Presenting results in various chart formats
- **Voice Interaction**: Basic voice command processing

Future expansions may include write operations (INSERT, UPDATE, DELETE), more complex query generation, and advanced voice conversation capabilities.

## Technical Architecture

The Natural Language to SQL Assistant follows a modular, service-oriented architecture that separates concerns and promotes maintainability. The system is structured into several key layers:

1. **Presentation Layer**: User interfaces for web and voice interaction
   - Streamlit-based web GUI
   - Voice command interface

2. **Application Layer**: Core business logic and services
   - Natural language processing
   - SQL generation
   - Database management
   - Voice processing

3. **Data Layer**: Database connections and schema management
   - Multi-database support
   - Schema extraction and formatting
   - Query execution

4. **Integration Layer**: External services and APIs
   - Speech recognition services
   - Text-to-speech services
   - Data visualization libraries

## System Flow

### Text Query Flow

1. **User Input**
   - User enters a natural language question through the web interface
   - Example: "Show me the top 5 customers by total order value"

2. **Query Processing**
   - The input is sent to the SQL Generator service
   - The service retrieves the current database schema from the Schema Reader
   - The schema and query are combined into a prompt for the Mistral-7B model
   - The model generates SQL based on the natural language and schema context

3. **SQL Execution**
   - The generated SQL is validated and formatted
   - The SQL is sent to the Database Manager for execution
   - The Database Manager executes the query against the connected database
   - Results are returned as structured data

4. **Result Presentation**
   - Results are displayed in a tabular format
   - If applicable, data visualization options are presented
   - Statistical summaries are generated for numerical data
   - The user can export results or create different visualizations

### Voice Query Flow

1. **Voice Activation**
   - User activates the voice assistant with the wake word "Hey Assistant"
   - The voice assistant enters listening mode

2. **Speech Recognition**
   - The voice input is captured through the microphone
   - The system attempts offline recognition with Vosk first
   - If offline recognition fails or has low confidence, online recognition is used
   - The recognized speech is converted to text

3. **Command Processing**
   - The text is analyzed to determine if it's a system command or a database query
   - System commands (e.g., "open settings") are handled directly
   - Database queries are processed through the standard text query flow

4. **Response Generation**
   - Results are prepared for voice response
   - For simple results, a text-to-speech summary is generated
   - For complex results, a brief summary is spoken and full results are displayed
   - The conversation history is updated

### Data Visualization Flow

1. **Data Analysis**
   - Query results are analyzed to determine appropriate visualization types
   - Numerical distributions, categorical comparisons, and time series are identified

2. **Chart Generation**
   - Based on data characteristics and user preferences, charts are generated
   - Plotly is used to create interactive visualizations
   - Chart options include bar charts, line charts, scatter plots, pie charts, and more

3. **User Interaction**
   - Users can modify chart parameters (type, colors, labels, etc.)
   - Interactive elements allow zooming, panning, and data point inspection
   - Multiple visualizations can be created from the same dataset

4. **Export and Sharing**
   - Visualizations can be exported as images or interactive HTML
   - Data can be exported in various formats (CSV, Excel, JSON)
   - Analysis results can be saved for future reference

### Component Interaction

The system follows these general interaction patterns:

1. **User Input Processing**:
   - Text input is processed directly by the NLP engine
   - Voice input is converted to text before processing

2. **Query Generation**:
   - Natural language is analyzed and transformed into SQL
   - Database schema information guides query generation
   - Generated SQL is validated and optimized

3. **Query Execution**:
   - SQL is executed against the connected database
   - Results are retrieved and formatted
   - Error handling and recovery mechanisms are applied

4. **Result Presentation**:
   - Data is displayed in tables and charts
   - Statistical analysis is performed on results
   - Voice responses are generated when appropriate

### Technology Stack

1. **Frontend**:
   - Streamlit: Web application framework
   - Plotly: Interactive data visualization
   - Custom CSS: Enhanced UI styling

2. **Backend**:
   - FastAPI: API framework for the service layer
   - SQLAlchemy: Database ORM and connection management
   - Pydantic: Data validation and settings management

3. **NLP & AI**:
   - Mistral-7B: Large language model for SQL generation
   - Transformers: NLP processing library
   - Accelerate/BitsAndBytes: Model optimization

4. **Voice Processing**:
   - Vosk: Offline speech recognition
   - SpeechRecognition: Online speech recognition
   - pyttsx3: Text-to-speech synthesis

5. **Data Analysis**:
   - Pandas: Data manipulation and analysis
   - NumPy: Numerical computing
   - SciPy: Scientific computing and statistics

6. **Database Support**:
   - SQLite: Default embedded database
   - PostgreSQL: Via psycopg2-binary
   - MySQL: Via pymysql
   - SQL Server: Via pyodbc
   - Oracle: Via cx-oracle

## Core Components

### 1. SQL Generator

The SQL Generator is the heart of the system, responsible for transforming natural language questions into valid SQL queries.

**Key Features**:
- Uses a Mistral-7B language model for natural language understanding
- Incorporates database schema information for context-aware query generation
- Formats and validates generated SQL for security and correctness
- Executes queries and returns structured results

**Implementation**:
- Located in `app/services/sql_generator.py`
- Implemented as a singleton class for efficient resource usage
- Uses prompt engineering with schema context for accurate SQL generation
- Integrates with database manager for query execution

## Implementation Details

### Natural Language to SQL Conversion

The core functionality of converting natural language to SQL is implemented using the Mistral-7B language model with carefully crafted prompts that include database schema information.

**Prompt Engineering**:

The system uses a template-based approach for prompt construction, combining:

1. **Task Description**: Clear instructions for SQL generation
2. **Schema Context**: Detailed database structure information
3. **User Query**: The natural language question
4. **Examples**: Few-shot examples of similar conversions (when available)

Example prompt structure:
```
You are an expert SQL query generator.
Given the following database schema:
{schema}

Generate a SQL query that answers the following question:
{question}

Return ONLY the SQL query without any explanation.
```

**SQL Validation and Formatting**:

Generated SQL undergoes several processing steps:

1. **Parsing**: Using `sqlparse` to validate syntax
2. **Formatting**: Standardizing indentation and keyword casing
3. **Security Checks**: Preventing SQL injection and dangerous operations
4. **Optimization**: Basic query optimization for performance

### Database Abstraction Layer

The Database Manager provides a unified interface for different database systems through SQLAlchemy.

**Connection String Generation**:

Each database type requires specific connection parameters:

- **SQLite**: Simple file path-based connection
- **PostgreSQL**: Host, port, database name, user, password
- **MySQL**: Similar to PostgreSQL with specific driver options
- **SQL Server**: Windows authentication or SQL authentication options
- **Oracle**: TNS name or direct connection parameters

**Connection Pooling**:

Connections are managed through SQLAlchemy's connection pooling:

- **Pool Size**: Configurable maximum connections
- **Overflow**: Handling peak demand
- **Timeout**: Connection acquisition timeout
- **Recycle**: Connection recycling after specified period

### Voice Processing System

The voice processing system uses a hybrid approach with multiple recognition engines.

**Speech Recognition**:

1. **Offline Recognition (Vosk)**:
   - Uses pre-downloaded models for offline processing
   - Lower latency but potentially lower accuracy
   - Works without internet connection

2. **Online Recognition (SpeechRecognition)**:
   - Uses cloud-based services for higher accuracy
   - Requires internet connection
   - Higher latency but better for complex queries

**Text-to-Speech**:

The pyttsx3 library provides offline text-to-speech capabilities:

- Voice selection based on available system voices
- Rate and volume adjustment
- Non-blocking operation for UI responsiveness

### Data Visualization Framework

The data visualization system uses Plotly for interactive charts and Pandas for data manipulation.

**Chart Generation Process**:

1. **Data Analysis**: Automatic detection of data types and relationships
2. **Chart Selection**: Intelligent selection of appropriate chart types
3. **Rendering**: Generation of interactive Plotly visualizations
4. **Customization**: User-configurable chart parameters

**Supported Chart Types**:

- **Bar Charts**: For categorical comparisons
- **Line Charts**: For time series and trends
- **Scatter Plots**: For correlation analysis
- **Pie Charts**: For part-to-whole relationships
- **Histograms**: For distribution analysis
- **Box Plots**: For statistical summaries
- **Heatmaps**: For matrix data visualization

### Web Interface Implementation

The web interface is built with Streamlit, providing a responsive and interactive user experience.

**UI Components**:

1. **Sidebar**: Database connection management and settings
2. **Query Input**: Text area and voice input button
3. **Results Area**: Tabular data display with sorting and filtering
4. **Visualization Tabs**: Multiple tabs for different visualization options
5. **Export Options**: Data and chart export functionality

**State Management**:

Streamlit's session state is used to maintain application state:

- Database connection information
- Query history
- Current results and visualizations
- User preferences and settings

**Custom Styling**:

Custom CSS is applied for a modern, professional appearance:

- Gradient backgrounds
- Custom card components
- Responsive layouts
- Consistent color scheme

### 2. Database Manager

The Database Manager handles all database connections and operations, providing a unified interface for different database types.

**Key Features**:
- Supports multiple database types (SQLite, PostgreSQL, MySQL, SQL Server, Oracle)
- Generates appropriate connection strings for each database type
- Manages connection pools and session handling
- Provides schema information extraction capabilities
- Executes SQL queries and returns results in a standardized format

**Implementation**:
- Located in `app/services/database_manager.py`
- Uses SQLAlchemy for database abstraction
- Implements connection pooling and timeout handling
- Provides detailed error reporting and connection diagnostics

### 3. Schema Reader

The Schema Reader extracts and formats database schema information, which is crucial for accurate SQL generation.

**Key Features**:
- Extracts table and column information from connected databases
- Formats schema information for use in NLP prompts
- Provides simplified schema summaries for UI display
- Detects relationships between tables

**Implementation**:
- Located in `app/services/schema_reader.py`
- Works with the Database Manager to extract schema information
- Formats schema in a structured way for both machine and human consumption

### 4. Enhanced Voice Assistant

The Enhanced Voice Assistant enables voice interaction with the system, providing a hands-free experience.

**Key Features**:
- Wake word detection ("Hey Assistant")
- Multiple speech recognition engines (Vosk for offline, SpeechRecognition for online)
- Natural language understanding for voice commands
- Text-to-speech response generation
- Conversation mode for continuous interaction

**Implementation**:
- Located in `app/services/enhanced_voice_assistant.py`
- Uses pyttsx3 for text-to-speech synthesis
- Implements fallback mechanisms between speech recognition engines
- Maintains conversation context and user preferences

### 5. Web Interface

The web interface provides a user-friendly way to interact with the system through a browser.

**Key Features**:
- Modern, responsive UI with gradient styling
- Interactive data visualization with multiple chart types
- Database schema display and exploration
- Voice command integration
- Advanced data analysis capabilities

**Implementation**:
- Located in `gui/enhanced_streamlit_app.py` and related files
- Built with Streamlit for rapid development
- Uses Plotly for interactive visualizations
- Implements session state management for user interactions

## Future Development

### Planned Enhancements

#### Write Operations Support

Future versions will extend beyond read-only operations to include:

- **Data Modification**: Support for INSERT, UPDATE, and DELETE operations
- **Transaction Management**: Handling multi-statement transactions
- **Validation Rules**: Configurable validation for write operations
- **Audit Trail**: Tracking of all data modifications

#### Advanced NLP Capabilities

Enhancements to the natural language processing system:

- **Context Awareness**: Maintain context across multiple queries
- **Ambiguity Resolution**: Interactive clarification of ambiguous queries
- **Domain-Specific Training**: Customization for specific industries or datasets
- **Multi-language Support**: Process queries in languages beyond English

#### Enhanced Voice Interaction

Improvements to the voice assistant:

- **Custom Wake Words**: User-definable activation phrases
- **Voice Identification**: Recognize different users by voice
- **Ambient Noise Adaptation**: Dynamically adjust to changing environments
- **Natural Conversation**: More human-like interaction patterns

#### Advanced Visualization and Analysis

Expanded data visualization and analysis capabilities:

- **Machine Learning Integration**: Automated pattern recognition and anomaly detection
- **Predictive Analytics**: Forecast future trends based on historical data
- **Custom Visualization Types**: User-defined chart types and visualizations
- **Dashboard Builder**: Drag-and-drop interface for custom dashboards

### Technical Roadmap

#### Performance Optimization

Planned improvements for system performance:

- **Query Caching**: Store and reuse common query results
- **Model Quantization**: Optimize LLM for faster inference
- **Parallel Processing**: Distribute workloads across multiple cores
- **Incremental Schema Updates**: Avoid full schema reloads

#### Scalability Enhancements

Features to support larger deployments:

- **Horizontal Scaling**: Support for distributed deployment
- **Load Balancing**: Distribute requests across multiple instances
- **Resource Management**: Dynamic allocation based on workload
- **High Availability**: Failover and redundancy features

#### Integration Capabilities

Expanded integration with other systems:

- **API Expansion**: More comprehensive REST API
- **Webhook Support**: Event-driven integration with external systems
- **ETL Capabilities**: Data extraction, transformation, and loading
- **Third-party Authentication**: Integration with OAuth providers

### API Service

The API service provides programmatic access to the system's capabilities.

**Key Features**:
- RESTful API for natural language to SQL conversion
- Schema information endpoints
- Voice query processing
- Rate limiting and security features

**Implementation**:
- Located in `app/main.py`
- Built with FastAPI for high performance
- Implements request validation and error handling
- Provides OpenAPI documentation

## Installation and Configuration

### System Requirements

**Hardware Requirements**:
- CPU: 4+ cores recommended for running the LLM
- RAM: Minimum 8GB, 16GB+ recommended
- Storage: 2GB for application and dependencies, additional space for databases
- GPU: Optional but recommended for faster LLM inference

**Software Requirements**:
- Python 3.8 or higher
- Operating System: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- Database System: At least one of SQLite, PostgreSQL, MySQL, SQL Server, or Oracle

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/nlp-to-sql-assistant.git
   cd nlp-to-sql-assistant
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Database Drivers**
   
   Depending on your database system, install the appropriate drivers:
   
   - SQLite: Included in Python standard library
   - PostgreSQL: `pip install psycopg2-binary`
   - MySQL: `pip install pymysql`
   - SQL Server: `pip install pyodbc`
   - Oracle: `pip install cx-oracle`

5. **Download Voice Models (Optional)**
   
   For offline voice recognition:
   ```bash
   # Create models directory
   mkdir -p app/models/vosk
   
   # Download a Vosk model (example for English)
   wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
   unzip vosk-model-small-en-us-0.15.zip -d app/models/vosk/
   ```

### Configuration

1. **Environment Variables**
   
   Create a `.env` file in the project root with the following variables:
   
   ```
   # Application Settings
   APP_ENV=development  # or production
   LOG_LEVEL=INFO
   
   # Database Default Connection (Optional)
   DEFAULT_DB_TYPE=sqlite  # or postgresql, mysql, sqlserver, oracle
   DEFAULT_DB_PATH=./data/default.db  # for SQLite
   # For other databases
   # DEFAULT_DB_HOST=localhost
   # DEFAULT_DB_PORT=5432
   # DEFAULT_DB_NAME=mydatabase
   # DEFAULT_DB_USER=myuser
   # DEFAULT_DB_PASSWORD=mypassword
   
   # Voice Settings
   ENABLE_VOICE=true
   VOICE_WAKE_WORD="Hey Assistant"
   ```

2. **Database Connection Presets**
   
   Create a `connection_presets.json` file in the `app/config` directory:
   
   ```json
   {
     "sample_sqlite": {
       "type": "sqlite",
       "path": "./data/sample.db",
       "description": "Sample SQLite Database"
     },
     "dev_postgresql": {
       "type": "postgresql",
       "host": "localhost",
       "port": 5432,
       "database": "devdb",
       "user": "devuser",
       "password": "devpassword",
       "description": "Development PostgreSQL Database"
     }
   }
   ```

3. **Application Settings**
   
   Modify `app/config/settings.py` to adjust application behavior:
   
   ```python
   # SQL Generation Settings
   SQL_GENERATION_TIMEOUT = 30  # seconds
   MAX_QUERY_RESULTS = 1000
   
   # Voice Settings
   VOICE_RATE = 150  # words per minute
   VOICE_VOLUME = 0.8  # 0.0 to 1.0
   
   # UI Settings
   DEFAULT_CHART_TYPE = "bar"
   DEFAULT_THEME = "light"  # or "dark"
   ```

### Running the Application

1. **Start the API Server**
   ```bash
   cd app
   uvicorn main:app --reload --port 8000
   ```

2. **Start the Web Interface**
   ```bash
   cd gui
   streamlit run enhanced_streamlit_app.py
   ```

3. **Access the Application**
   
   Open your web browser and navigate to:
   - Web Interface: http://localhost:8501
   - API Documentation: http://localhost:8000/docs

## Advanced Features

### Enhanced Data Analysis Capabilities

#### Interactive Dashboard

The system provides a comprehensive interactive dashboard for data analysis:

- **Multi-view Analysis**: Simultaneously view data in different formats (tables, charts, statistics)
- **Real-time Filtering**: Filter and sort data without regenerating queries
- **Drill-down Capabilities**: Click on chart elements to explore underlying data
- **Custom Layouts**: Save and load personalized dashboard configurations

#### Advanced Visualization Features

Beyond basic charts, the system offers advanced visualization capabilities:

- **Multi-series Charts**: Compare multiple data series in a single visualization
- **Combination Charts**: Mix chart types (e.g., bar and line) for multi-dimensional analysis
- **Geospatial Visualization**: Map-based visualizations for geographical data
- **Interactive Elements**: Tooltips, zoom controls, and click-through actions
- **Animation**: Animated transitions for time-series data

#### Statistical Analysis Tools

The system includes built-in statistical analysis features:

- **Descriptive Statistics**: Mean, median, mode, standard deviation, etc.
- **Correlation Analysis**: Identify relationships between variables
- **Trend Detection**: Automatic identification of trends in time-series data
- **Outlier Detection**: Highlight anomalous data points
- **Forecasting**: Simple predictive models for time-series data

### Voice Assistant Capabilities

#### Multi-Engine Speech Recognition

The voice system uses a hybrid approach for optimal performance:

- **Offline Processing**: Vosk-based recognition for privacy and reliability
- **Online Processing**: Cloud-based recognition for higher accuracy
- **Automatic Fallback**: Seamless switching between engines based on confidence scores
- **Noise Filtering**: Advanced algorithms to improve recognition in noisy environments

#### Natural Language Understanding

The voice assistant can understand various command types:

- **Database Commands**: Query generation and execution
- **System Commands**: Application control and navigation
- **Analysis Commands**: Visualization and statistical analysis requests
- **Context-aware Responses**: Maintains conversation context for follow-up questions

#### Conversation Mode

The assistant supports continuous conversation:

- **Wake Word Detection**: Activate with "Hey Assistant" without clicking buttons
- **Active Listening**: Remain in listening mode for follow-up questions
- **Interruption Handling**: Allow users to interrupt responses
- **Conversation History**: Track and reference previous interactions

### Security Features

#### SQL Injection Prevention

The system implements multiple layers of protection against SQL injection:

- **Query Validation**: Parsing and validation of generated SQL
- **Parameterized Queries**: Use of SQLAlchemy's parameterization
- **Blacklisted Operations**: Prevention of dangerous operations (DROP, DELETE without WHERE, etc.)
- **Schema Restriction**: Limiting access to specified tables and views

#### Authentication and Authorization

The system includes security features for multi-user environments:

- **User Authentication**: Username/password or SSO integration
- **Role-based Access**: Different permission levels for users
- **Connection Isolation**: Separate database connections per user
- **Audit Logging**: Tracking of all queries and actions

#### Data Protection

Sensitive data is protected through various mechanisms:

- **Data Masking**: Automatic masking of sensitive fields (e.g., PII)
- **Encryption**: Secure storage of connection credentials
- **Secure Connections**: SSL/TLS for database connections
- **Session Management**: Automatic timeout and secure session handling

### Multi-Database Support

#### Connection Management

The system provides robust database connection handling:

- **Connection Pooling**: Efficient reuse of database connections
- **Auto-reconnect**: Automatic handling of connection drops
- **Connection Presets**: Save and quickly switch between databases
- **Connection Testing**: Validate connections before use

#### Database-Specific Optimizations

The system adapts to different database engines:

- **Dialect-specific SQL**: Generate optimized SQL for each database type
- **Feature Detection**: Adapt to available features in each database
- **Performance Tuning**: Database-specific query optimization
- **Error Handling**: Customized error messages for different databases

#### Schema Management

Advanced schema handling capabilities:

- **Automatic Schema Detection**: Discover tables, views, and relationships
- **Schema Caching**: Store schema information for faster startup
- **Schema Updates**: Detect and adapt to schema changes
- **Metadata Enrichment**: Add descriptions and usage hints to schema elements

## Troubleshooting and FAQ

### Usage Guide

#### Connecting to Databases

1. **Using the Connection Interface**
   
   - Navigate to the sidebar in the web interface
   - Select "Database Connection" section
   - Choose a connection preset or enter connection details manually
   - Click "Connect" to establish the database connection

2. **Managing Connection Presets**
   
   - Click "Manage Presets" in the connection section
   - Add new presets by providing connection details and a name
   - Edit or delete existing presets
   - Test connections before saving

3. **Connection Troubleshooting**
   
   - Check that the database server is running and accessible
   - Verify credentials and connection parameters
   - Ensure required database drivers are installed
   - Check firewall settings if connecting to remote databases

#### Text-Based Queries

1. **Basic Queries**
   
   Enter natural language questions in the query input box:
   
   - "Show me all customers from New York"
   - "What are the top 5 products by sales?"
   - "How many orders were placed last month?"

2. **Advanced Queries**
   
   The system supports complex analytical questions:
   
   - "Calculate the average order value by customer segment"
   - "Show me the trend of monthly sales for the past year"
   - "Find products that have never been ordered"

3. **Query Refinement**
   
   If results aren't as expected:
   
   - Add more specific details to your question
   - Reference specific table or column names if known
   - Check the generated SQL and modify if needed

#### Voice Interaction

1. **Activating Voice Mode**
   
   - Click the microphone button or say "Hey Assistant"
   - Wait for the "Listening..." indicator
   - Speak your query clearly

2. **Voice Commands**
   
   Common voice commands include:
   
   - "Show schema" - Displays database structure
   - "Connect to [database name]" - Changes database connection
   - "Visualize as [chart type]" - Changes visualization
   - "Export results to CSV" - Exports current results

3. **Conversation Mode**
   
   - Enable conversation mode in settings
   - The assistant will remain active after responding
   - Say "Stop listening" to exit conversation mode

#### Data Visualization

1. **Selecting Chart Types**
   
   After query execution, select from available chart types:
   
   - Bar Chart: For categorical comparisons
   - Line Chart: For time series data
   - Scatter Plot: For correlation analysis
   - Pie Chart: For part-to-whole relationships
   - Histogram: For distribution analysis

2. **Customizing Visualizations**
   
   - Select columns for X and Y axes
   - Choose grouping and aggregation methods
   - Adjust colors, labels, and legends
   - Toggle grid lines and other display options

3. **Advanced Analysis**
   
   - Enable statistical analysis for numerical data
   - View trend lines and forecasts
   - Perform correlation analysis between variables
   - Generate summary statistics

#### Exporting and Sharing

1. **Data Export Options**
   
   Export query results in various formats:
   
   - CSV: For spreadsheet applications
   - Excel: For Microsoft Excel
   - JSON: For programmatic use
   - SQL: The generated query for reuse

2. **Chart Export**
   
   Save visualizations as:
   
   - PNG: Static image
   - SVG: Vector graphic
   - HTML: Interactive web page
   - PDF: Document format

3. **Saving Analysis**
   
   - Save the current analysis configuration
   - Include query, visualization settings, and notes
   - Reload saved analyses from the library