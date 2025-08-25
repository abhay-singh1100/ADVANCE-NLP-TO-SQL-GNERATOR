import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Optional, Any
import sys
import os
import json
import time
import threading
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.sql_generator import get_generator
from app.services.schema_reader import SchemaReader
from app.services.enhanced_voice_assistant import get_enhanced_assistant
from app.services.database_manager import get_db_manager

# Initialize services
sql_generator = get_generator()
schema_reader = SchemaReader()
voice_assistant = get_enhanced_assistant()
db_manager = get_db_manager()

# Page config
st.set_page_config(
    page_title="AI Voice Assistant & Data Analysis",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    .voice-controls {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .sql-box {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        font-size: 1.1em;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .conversation-bubble {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .user-bubble {
        background: #e3f2fd;
        border-left-color: #2196f3;
        text-align: right;
    }
    .assistant-bubble {
        background: #f3e5f5;
        border-left-color: #9c27b0;
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-listening {
        background-color: #4caf50;
        animation: pulse 1.5s infinite;
    }
    .status-idle {
        background-color: #9e9e9e;
    }
    .status-processing {
        background-color: #ff9800;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .voice-button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        border: none;
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.2em;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .voice-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    .voice-button:active {
        transform: translateY(0);
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("""
    <div class="main-header">
        <h1>🎤 AI Voice Assistant & Data Analysis</h1>
        <p style="font-size: 1.3em; margin: 0;">Your intelligent voice-controlled assistant for database queries, data analysis, and system commands!</p>
        <p style="font-size: 1.1em; margin: 0.5rem 0 0 0;">Just say "Hey Assistant" to get started</p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'voice_status' not in st.session_state:
    st.session_state.voice_status = 'idle'  # idle, listening, processing
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'current_query' not in st.session_state:
    st.session_state.current_query = ""
if 'last_response' not in st.session_state:
    st.session_state.last_response = None
if 'is_conversation_mode' not in st.session_state:
    st.session_state.is_conversation_mode = False
if 'wake_word' not in st.session_state:
    st.session_state.wake_word = "hey assistant"

# Database Connection Status
if db_manager.is_connected():
    conn_info = db_manager.get_connection_info()
    st.success(f"✅ Connected to {conn_info['type'].upper()} database")
else:
    st.warning("⚠️ No database connected. Please connect to a database in the sidebar to get started.")

# Voice Controls Section
st.markdown("""
    <div class="voice-controls">
        <h2>🎤 Voice Controls</h2>
        <p>Control your assistant with voice commands or use the buttons below</p>
    </div>
""", unsafe_allow_html=True)

# Voice Control Buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🎤 Start Listening", key="start_listening", use_container_width=True):
        st.session_state.voice_status = 'listening'
        st.session_state.current_query = ""
        st.rerun()

with col2:
    if st.button("🔄 Conversation Mode", key="conversation_mode", use_container_width=True):
        st.session_state.is_conversation_mode = not st.session_state.is_conversation_mode()
        if st.session_state.is_conversation_mode:
            st.session_state.voice_status = 'listening'
        else:
            st.session_state.voice_status = 'idle'
        st.rerun()

with col3:
    if st.button("🔊 Test Voice", key="test_voice", use_container_width=True):
        voice_assistant.speak("Hello! I'm your voice assistant. I'm ready to help you with database queries, data analysis, and system commands.")

with col4:
    if st.button("⚙️ Settings", key="voice_settings", use_container_width=True):
        st.session_state.show_settings = True

# Voice Status Display
status_col1, status_col2 = st.columns([1, 3])

with status_col1:
    status_color = {
        'idle': 'status-idle',
        'listening': 'status-listening',
        'processing': 'status-processing'
    }
    
    st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 1rem 0;">
            <span class="status-indicator {status_color[st.session_state.voice_status]}"></span>
            <strong>Status: {st.session_state.voice_status.title()}</strong>
        </div>
    """, unsafe_allow_html=True)

with status_col2:
    if st.session_state.voice_status == 'listening':
        st.info("🎧 Listening for your command... Say 'Hey Assistant' followed by your request")
    elif st.session_state.voice_status == 'processing':
        st.info("🤔 Processing your request...")
    else:
        st.info("💤 Ready to listen. Click 'Start Listening' or say the wake word")

# Voice Input Section
st.markdown("### 🎯 Voice Command Input")

# Manual input as fallback
manual_input = st.text_input(
    "Type your command here (or use voice):",
    value=st.session_state.current_query,
    placeholder="e.g., 'Show me the data from the users table' or 'Analyze trends in sales data'",
    key="manual_input"
)

if manual_input != st.session_state.current_query:
    st.session_state.current_query = manual_input

# Process voice command
if st.button("🚀 Process Command", key="process_command", use_container_width=True):
    if st.session_state.current_query:
        st.session_state.voice_status = 'processing'
        st.rerun()
        
        # Process the command
        response = voice_assistant.process_command(st.session_state.current_query)
        st.session_state.last_response = response
        
        # Add to conversation history
        st.session_state.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': st.session_state.current_query,
            'assistant': response['response_text'],
            'action': response['action'],
            'data': response['data']
        })
        
        st.session_state.voice_status = 'idle'
        st.session_state.current_query = ""
        st.rerun()

# Voice Command Examples
with st.expander("💡 Voice Command Examples"):
    st.markdown("""
    **Database Queries:**
    - "Show me all users from the database"
    - "Display the sales data for last month"
    - "Create a SQL query to find active customers"
    - "Analyze the user registration trends"
    
    **Data Analysis:**
    - "Find patterns in the sales data"
    - "Compare performance between regions"
    - "Show me statistics for user engagement"
    - "Identify outliers in the dataset"
    
    **System Commands:**
    - "Open calculator"
    - "Search for Python tutorials on the web"
    - "Launch notepad"
    - "Help me with database queries"
    
    **General Conversation:**
    - "Hello, how are you?"
    - "What can you help me with?"
    - "Thank you for your help"
    - "Goodbye"
    """)

# Process voice input if status is listening
if st.session_state.voice_status == 'listening':
    # Simulate voice input processing
    if st.button("🎤 Simulate Voice Input", key="simulate_voice"):
        # For demonstration, we'll use a sample command
        sample_commands = [
            "Show me the data from the users table",
            "Analyze trends in sales data",
            "Open calculator",
            "Search for Python tutorials",
            "Hello, how are you?"
        ]
        
        import random
        sample_command = random.choice(sample_commands)
        st.session_state.current_query = sample_command
        st.session_state.voice_status = 'processing'
        st.rerun()

# Display last response
if st.session_state.last_response:
    st.markdown("### 📋 Last Command Response")
    
    response = st.session_state.last_response
    
    # Display response details
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.info(f"**Action:** {response['action']}")
        st.success(f"**Command:** {response['command']}")
    
    with col2:
        st.warning(f"**Response Type:** {response['data'].get('query_type', 'unknown')}")
        if 'app_name' in response['data']:
            st.info(f"**Application:** {response['data']['app_name']}")
        if 'search_query' in response['data']:
            st.info(f"**Search Query:** {response['data']['search_query']}")
    
    # Display full response
    st.markdown("**Full Response:**")
    st.markdown(f"<div class='assistant-bubble'>{response['response_text']}</div>", unsafe_allow_html=True)

# Conversation History
if st.session_state.conversation_history:
    st.markdown("### 💬 Conversation History")
    
    # Filter options
    col1, col2 = st.columns([1, 1])
    
    with col1:
        show_all = st.checkbox("Show all conversations", value=True)
    
    with col2:
        if st.button("🗑️ Clear History", key="clear_history"):
            st.session_state.conversation_history = []
            st.rerun()
    
    # Display conversation history
    if st.session_state.conversation_history:
        for i, entry in enumerate(reversed(st.session_state.conversation_history[-10:] if not show_all else st.session_state.conversation_history)):
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%H:%M:%S")
            
            st.markdown(f"""
                <div style="margin: 1rem 0;">
                    <small style="color: #666;">{timestamp}</small>
                    <div class="user-bubble">
                        <strong>You:</strong> {entry['user']}
                    </div>
                    <div class="assistant-bubble">
                        <strong>Assistant:</strong> {entry['assistant']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Settings Section
if st.session_state.get('show_settings', False):
    st.markdown("### ⚙️ Voice Assistant Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_wake_word = st.text_input("Wake Word:", value=st.session_state.wake_word)
        if st.button("Update Wake Word"):
            voice_assistant.set_wake_word(new_wake_word)
            st.session_state.wake_word = new_wake_word
            st.success(f"Wake word updated to: {new_wake_word}")
    
    with col2:
        speech_rate = st.slider("Speech Rate:", min_value=100, max_value=300, value=160, step=10)
        speech_volume = st.slider("Speech Volume:", min_value=0.0, max_value=1.0, value=0.9, step=0.1)
        
        if st.button("Update Voice Preferences"):
            voice_assistant.set_voice_preferences(rate=speech_rate, volume=speech_volume)
            st.success("Voice preferences updated!")
    
    if st.button("Close Settings"):
        st.session_state.show_settings = False
        st.rerun()

# Database Analysis Section (if connected)
if db_manager.is_connected():
    st.markdown("### 🗄️ Database Analysis")
    
    # Get available tables
    try:
        tables = schema_reader.get_tables()
        
        if tables:
            selected_table = st.selectbox("Select a table to analyze:", tables)
            
            if selected_table:
                # Get table schema
                schema = schema_reader.get_table_schema(selected_table)
                
                if schema:
                    st.markdown(f"**Table Schema for {selected_table}:**")
                    schema_df = pd.DataFrame(schema)
                    st.dataframe(schema_df, use_container_width=True)
                    
                    # Voice command suggestion
                    st.info(f"💡 Try saying: 'Show me data from the {selected_table} table' or 'Analyze the {selected_table} table'")
                    
                    # Sample data preview
                    if st.button(f"Preview {selected_table} data"):
                        try:
                            sample_data = db_manager.execute_query(f"SELECT * FROM {selected_table} LIMIT 10")
                            if sample_data:
                                st.dataframe(sample_data, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error previewing data: {str(e)}")
        else:
            st.warning("No tables found in the connected database.")
            
    except Exception as e:
        st.error(f"Error reading database schema: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🎤 AI Voice Assistant powered by Vosk & SpeechRecognition</p>
        <p>Say "Hey Assistant" to activate voice commands</p>
    </div>
""", unsafe_allow_html=True)

# Auto-refresh for conversation mode
if st.session_state.is_conversation_mode:
    time.sleep(2)
    st.rerun()
