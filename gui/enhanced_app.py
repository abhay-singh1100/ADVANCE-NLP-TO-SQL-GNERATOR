import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Optional, Any
import sys
import os
import requests
import json
from io import BytesIO
import base64
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.sql_generator import get_generator
from app.services.schema_reader import SchemaReader
from app.services.voice_service import get_voice_service
from app.services.database_manager import get_db_manager

# Initialize services
sql_generator = get_generator()
schema_reader = SchemaReader()
voice_service = get_voice_service()

# Page config
st.set_page_config(
    page_title="Advanced Data Analysis & SQL Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .sql-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        font-size: 1.1em;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("""
    <div class="main-header">
        <h1>📊 Advanced Data Analysis & SQL Assistant</h1>
        <p style="font-size: 1.2em; margin: 0;">Transform natural language into powerful SQL queries with advanced analytics, interactive visualizations, and comprehensive data insights!</p>
    </div>
""", unsafe_allow_html=True)

# Database Connection Status
db_manager = get_db_manager()
if db_manager.is_connected():
    conn_info = db_manager.get_connection_info()
    st.success(f"✅ Connected to {conn_info['type'].upper()} database")
else:
    st.warning("⚠️ No database connected. Please connect to a database in the sidebar to get started.")

# Initialize session state
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'voice_query' not in st.session_state:
    st.session_state.voice_query = None
if 'last_query' not in st.session_state:
    st.session_state.last_query = None
if 'last_sql' not in st.session_state:
    st.session_state.last_sql = None
if 'last_results' not in st.session_state:
    st.session_state.last_results = None
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None

# Create input area
input_container = st.container()

with input_container:
    input_col, mic_col = st.columns([6, 1])
    
    with input_col:
        query = st.text_input(
            "🔍 Ask your data question:",
            placeholder="e.g., 'Show total sales by city with trend analysis' or 'What are the top 10 products by revenue with profit margins?'",
            value=st.session_state.voice_query if st.session_state.voice_query else ""
        )
    
    with mic_col:
        st.markdown("<br>", unsafe_allow_html=True)
        mic_button = st.button("🎤", key="mic_button", help="Click to start/stop voice recording")

# Handle voice recording
if mic_button:
    if not st.session_state.is_recording:
        st.session_state.is_recording = True
        st.session_state.voice_query = None
        
        with st.spinner("🎤 Listening..."):
            try:
                query = voice_service.process_voice_query()
                if query:
                    st.session_state.voice_query = query
                    st.experimental_rerun()
            except Exception as e:
                st.error(f"Error processing voice input: {str(e)}")
            finally:
                st.session_state.is_recording = False

# Sidebar
with st.sidebar:
    # Database Connection Section
    st.header("🔌 Database Connection")
    
    # Import database connection functionality
    from gui.database_connection import render_database_connection, initialize_default_connection
    
    # Initialize default connection
    initialize_default_connection()
    
    # Render database connection interface
    render_database_connection()
    
    st.markdown("---")
    
    # Database Schema Section
    st.header("📊 Database Schema")
    
    # Check if database is connected before showing schema
    db_manager = get_db_manager()
    if db_manager.is_connected():
        try:
            schema_summary = schema_reader.get_schema_summary()
            
            for table_name, columns in schema_summary.items():
                with st.expander(f"📋 {table_name}"):
                    for column in columns:
                        st.text(f"• {column}")
        except Exception as e:
            st.error(f"❌ Error reading schema: {str(e)}")
            st.info("💡 Please check your database connection")
    else:
        st.warning("⚠️ No database connected")
        st.info("💡 Connect to a database above to view schema")
    
    st.markdown("---")
    st.header("⚙️ Analysis Options")
    
    chart_types = ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram", "Box Plot"]
    selected_charts = st.multiselect(
        "Select chart types:",
        chart_types,
        default=["Bar Chart", "Line Chart"]
    )
    
    analysis_depth = st.selectbox(
        "Analysis depth:",
        ["Basic", "Intermediate", "Advanced", "Expert"]
    )
    
    export_format = st.selectbox(
        "Export format:",
        ["CSV", "Excel", "JSON", "HTML"]
    )

# Process query
if query and query != st.session_state.last_query:
    # Check if database is connected
    if not db_manager.is_connected():
        st.error("❌ No database connected. Please connect to a database first.")
    else:
        try:
            with st.spinner("🚀 Generating SQL and executing query..."):
                # Generate and execute SQL
                sql, results = sql_generator.generate_and_execute(query)
                
                # Store results in session state
                st.session_state.last_query = query
                st.session_state.last_sql = sql
                st.session_state.last_results = results
                st.session_state.voice_query = None
                
                # Prepare data for analysis
                if results:
                    df = pd.DataFrame(results)
                    st.session_state.analysis_data = df
                    
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.session_state.last_query = None
            st.session_state.last_sql = None
            st.session_state.last_results = None

# Display results
if st.session_state.last_sql and st.session_state.last_results and db_manager.is_connected():
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Results & Charts", 
        "🔍 Data Analysis", 
        "📈 Advanced Visualizations", 
        "📋 Data Export", 
        "💡 Insights & Recommendations"
    ])
    
    with tab1:
        st.markdown("### 🎯 Generated SQL Query")
        st.markdown(f'<div class="sql-box">{st.session_state.last_sql}</div>', 
                   unsafe_allow_html=True)
        
        if st.session_state.analysis_data is not None:
            df = st.session_state.analysis_data
            
            # Metrics
            total_rows = len(df)
            total_cols = len(df.columns)
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown("""
                    <div class="metric-card">
                        <h3>📊 Total Rows</h3>
                        <h2 style="color: #667eea;">{}</h2>
                    </div>
                """.format(total_rows), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                    <div class="metric-card">
                        <h3>📋 Total Columns</h3>
                        <h2 style="color: #667eea;">{}</h2>
                    </div>
                """.format(total_cols), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                    <div class="metric-card">
                        <h3>🔢 Numeric Columns</h3>
                        <h2 style="color: #667eea;">{}</h2>
                    </div>
                """.format(len(numeric_cols)), unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                    <div class="metric-card">
                        <h3>📝 Categorical Columns</h3>
                        <h2 style="color: #667eea;">{}</h2>
                    </div>
                """.format(len(categorical_cols)), unsafe_allow_html=True)
            
            # Data table
            st.markdown("### 📋 Interactive Data Table")
            st.dataframe(df, use_container_width=True, height=400)
            
            # Charts
            if selected_charts:
                st.markdown("### 📈 Generated Charts")
                
                if len(selected_charts) > 1:
                    fig = make_subplots(
                        rows=len(selected_charts), 
                        cols=1,
                        subplot_titles=selected_charts,
                        vertical_spacing=0.1
                    )
                    
                    for i, chart_type in enumerate(selected_charts):
                        row = i + 1
                        
                        if chart_type == "Bar Chart" and len(numeric_cols) > 0:
                            x_col = df.columns[0] if len(df.columns) > 0 else None
                            y_col = numeric_cols[0] if numeric_cols else None
                            if x_col and y_col:
                                fig.add_trace(
                                    go.Bar(x=df[x_col], y=df[y_col], name=f"{y_col} by {x_col}"),
                                    row=row, col=1
                                )
                        
                        elif chart_type == "Line Chart" and len(numeric_cols) > 0:
                            x_col = df.columns[0] if len(df.columns) > 0 else None
                            y_col = numeric_cols[0] if numeric_cols else None
                            if x_col and y_col:
                                fig.add_trace(
                                    go.Scatter(x=df[x_col], y=df[y_col], mode='lines+markers', name=f"{y_col} over {x_col}"),
                                    row=row, col=1
                                )
                    
                    fig.update_layout(height=300 * len(selected_charts), showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                
                else:
                    chart_type = selected_charts[0]
                    
                    if chart_type == "Bar Chart" and len(numeric_cols) > 0:
                        x_col = df.columns[0] if len(df.columns) > 0 else None
                        y_col = numeric_cols[0] if numeric_cols else None
                        if x_col and y_col:
                            fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                            st.plotly_chart(fig, use_container_width=True)
                    
                    elif chart_type == "Line Chart" and len(numeric_cols) > 0:
                        x_col = df.columns[0] if len(df.columns) > 0 else None
                        y_col = numeric_cols[0] if numeric_cols else None
                        if x_col and y_col:
                            fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} over {x_col}")
                            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 🔍 Data Analysis Dashboard")
        
        if st.session_state.analysis_data is not None:
            df = st.session_state.analysis_data
            
            # Statistical summary
            st.markdown("#### 📊 Statistical Summary")
            if len(numeric_cols) > 0:
                numeric_df = df[numeric_cols]
                st.dataframe(numeric_df.describe(), use_container_width=True)
            
            # Data quality analysis
            st.markdown("#### 🧹 Data Quality Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                missing_data = df.isnull().sum()
                if missing_data.sum() > 0:
                    st.markdown("**Missing Values:**")
                    missing_df = pd.DataFrame({
                        'Column': missing_data.index,
                        'Missing Count': missing_data.values,
                        'Missing %': (missing_data.values / len(df) * 100).round(2)
                    })
                    st.dataframe(missing_df, use_container_width=True)
                else:
                    st.success("✅ No missing values found!")
            
            with col2:
                st.markdown("**Data Types:**")
                dtype_df = pd.DataFrame({
                    'Column': df.columns,
                    'Data Type': df.dtypes.astype(str),
                    'Unique Values': [df[col].nunique() for col in df.columns]
                })
                st.dataframe(dtype_df, use_container_width=True)
            
            # Correlation analysis
            if len(numeric_cols) > 1:
                st.markdown("#### 🔗 Correlation Analysis")
                corr_matrix = df[numeric_cols].corr()
                
                fig = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    aspect="auto",
                    title="Correlation Matrix Heatmap"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(corr_matrix.round(3), use_container_width=True)
    
    with tab3:
        st.markdown("### 📈 Advanced Visualizations")
        
        if st.session_state.analysis_data is not None:
            df = st.session_state.analysis_data
            
            st.markdown("#### 🎨 Chart Customization")
            
            col1, col2 = st.columns(2)
            
            with col1:
                chart_type = st.selectbox(
                    "Select chart type:",
                    ["3D Scatter", "Bubble Chart", "Radar Chart", "Treemap", "Violin Plot"]
                )
            
            with col2:
                if len(numeric_cols) > 0:
                    x_axis = st.selectbox("X-axis:", df.columns, index=0)
                    y_axis = st.selectbox("Y-axis:", numeric_cols, index=0)
                else:
                    x_axis = st.selectbox("X-axis:", df.columns, index=0)
                    y_axis = st.selectbox("Y-axis:", df.columns, index=1)
            
            # Generate advanced charts
            if chart_type == "3D Scatter" and len(numeric_cols) >= 3:
                z_axis = st.selectbox("Z-axis:", numeric_cols, index=2)
                fig = px.scatter_3d(
                    df, x=x_axis, y=y_axis, z=z_axis,
                    title=f"3D Scatter Plot: {x_axis} vs {y_axis} vs {z_axis}"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "Bubble Chart" and len(numeric_cols) >= 3:
                size_col = st.selectbox("Size column:", numeric_cols, index=2)
                fig = px.scatter(
                    df, x=x_axis, y=y_axis, size=size_col,
                    title=f"Bubble Chart: {x_axis} vs {y_axis} (size: {size_col})"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 📋 Data Export & Download")
        
        if st.session_state.analysis_data is not None:
            df = st.session_state.analysis_data
            
            st.markdown("#### 💾 Export Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                if export_format == "Excel":
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name='Data', index=False)
                    
                    buffer.seek(0)
                    st.download_button(
                        label="📥 Download Excel",
                        data=buffer.getvalue(),
                        file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            
            with col2:
                if export_format == "JSON":
                    json_str = df.to_json(orient='records', indent=2)
                    st.download_button(
                        label="📥 Download JSON",
                        data=json_str,
                        file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                if export_format == "HTML":
                    html_str = df.to_html(index=False, classes='table table-striped')
                    st.download_button(
                        label="📥 Download HTML",
                        data=html_str,
                        file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html"
                    )
    
    with tab5:
        st.markdown("### 💡 Insights & Recommendations")
        
        if st.session_state.analysis_data is not None:
            df = st.session_state.analysis_data
            
            st.markdown("#### 🧠 AI-Generated Insights")
            
            if len(numeric_cols) > 0:
                st.markdown("**🔍 Data Patterns:**")
                
                # Outlier detection
                outlier_insights = []
                for col in numeric_cols:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
                    
                    if len(outliers) > 0:
                        outlier_insights.append(f"• **{col}**: {len(outliers)} outliers detected ({(len(outliers)/len(df)*100):.1f}% of data)")
                
                if outlier_insights:
                    st.warning("⚠️ **Outlier Detection:**")
                    for insight in outlier_insights:
                        st.write(insight)
                else:
                    st.success("✅ No significant outliers detected in numeric columns")
            
            # Data quality insights
            st.markdown("**🧹 Data Quality Insights:**")
            
            missing_percentage = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            if missing_percentage > 10:
                st.warning(f"⚠️ High missing data rate: {missing_percentage:.1f}%")
            elif missing_percentage > 5:
                st.info(f"ℹ️ Moderate missing data rate: {missing_percentage:.1f}%")
            else:
                st.success(f"✅ Low missing data rate: {missing_percentage:.1f}%")
            
            # Recommendations
            st.markdown("**💡 Recommendations:**")
            
            if len(numeric_cols) > 1:
                st.write("• Consider correlation analysis for numeric variables")
                st.write("• Use scatter plots to identify relationships")
            
            if len(categorical_cols) > 0:
                st.write("• Analyze categorical variable distributions")
                st.write("• Consider grouping strategies for analysis")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>🚀 Built with advanced analytics using Streamlit, Plotly, Pandas, and AI-powered SQL generation</p>
        <p>📊 Features: Interactive Visualizations • Advanced Analytics • Data Export • Statistical Analysis • AI Insights</p>
    </div>
""", unsafe_allow_html=True)
