# 🎤 Enhanced AI Voice Assistant

A comprehensive, voice-controlled AI assistant that combines natural language processing, database management, and system control capabilities. Transform your voice into powerful commands for data analysis, database queries, and system operations.

## ✨ Features

### 🎯 **Core Voice Capabilities**
- **Wake Word Detection**: Say "Hey Assistant" to activate
- **Multi-Engine Recognition**: Uses both Vosk (offline) and Google Speech Recognition (online)
- **Natural Language Understanding**: Processes complex voice commands with context awareness
- **Conversation Mode**: Continuous interaction without repeated wake words

### 🗄️ **Database & Data Analysis**
- **Voice SQL Generation**: "Show me data from the users table"
- **Schema Exploration**: "Describe the sales table structure"
- **Data Analysis**: "Find trends in customer data"
- **Query Optimization**: "Create a query to find active users"

### 💻 **System Control**
- **Application Launch**: "Open calculator" or "Launch notepad"
- **Web Search**: "Search for Python tutorials"
- **File Operations**: "Open documents folder"
- **System Information**: "Show system status"

### 🎨 **User Experience**
- **Modern Web Interface**: Beautiful Streamlit-based GUI
- **Real-time Status**: Visual indicators for listening, processing, and idle states
- **Conversation History**: Track all interactions with timestamps
- **Customizable Settings**: Adjust wake word, speech rate, and volume

## 🚀 Quick Start

### 1. **Installation**

```bash
# Clone or navigate to your project directory
cd nlp

# Install required packages
pip install -r requirements_voice.txt

# For Windows users, you might need:
pip install PyAudio
```

### 2. **Download Voice Models**

```bash
# Download Vosk model for offline recognition
python scripts/download_vosk_model.py

# Or manually download from:
# https://alphacephei.com/vosk/models
# Extract to: models/vosk-model-small-en-us-0.15/
```

### 3. **Launch the Assistant**

```bash
# Run the launcher script
python run_voice_assistant.py

# Or directly with Streamlit
streamlit run gui/enhanced_voice_app.py
```

### 4. **Start Using Voice Commands**

1. **Wake the Assistant**: Say "Hey Assistant"
2. **Give Commands**: "Show me the database tables"
3. **Get Responses**: The assistant will speak and display results
4. **Continue Conversation**: Use conversation mode for continuous interaction

## 🎤 Voice Command Examples

### **Database Operations**
```
"Show me all users from the database"
"Display sales data for last month"
"Create a SQL query to find active customers"
"Analyze user registration trends"
"Describe the table structure"
```

### **Data Analysis**
```
"Find patterns in the sales data"
"Compare performance between regions"
"Show me statistics for user engagement"
"Identify outliers in the dataset"
"Generate a summary report"
```

### **System Commands**
```
"Open calculator"
"Launch notepad"
"Search for Python tutorials on the web"
"Open the documents folder"
"Show system information"
```

### **General Interaction**
```
"Hello, how are you?"
"What can you help me with?"
"Thank you for your help"
"Goodbye"
"Help me with database queries"
```

## 🏗️ Architecture

### **Core Components**

```
EnhancedVoiceAssistant
├── Speech Recognition (Vosk + Google SR)
├── Text-to-Speech (pyttsx3)
├── Natural Language Processing
├── Command Intent Analysis
├── Response Generation
└── Context Management
```

### **Service Integration**

```
Voice Assistant → SQL Generator → Database Manager
              → Schema Reader → Table Analysis
              → System Commands → OS Integration
              → Web Search → Browser Control
```

## ⚙️ Configuration

### **Voice Settings**
- **Wake Word**: Customizable activation phrase
- **Speech Rate**: Adjust speaking speed (100-300 WPM)
- **Volume**: Control output volume (0.0-1.0)
- **Voice Selection**: Choose from available system voices

### **Recognition Settings**
- **Confidence Threshold**: Minimum confidence for command acceptance
- **Timeout Settings**: Adjust listening and phrase time limits
- **Audio Quality**: Configure sample rate and audio processing

### **User Preferences**
- **Conversation History**: Enable/disable logging
- **Auto-save**: Save preferences automatically
- **Custom Commands**: Add personalized voice shortcuts

## 🔧 Troubleshooting

### **Common Issues**

#### **Audio Not Working**
```bash
# Check audio devices
python -c "import sounddevice as sd; print(sd.query_devices())"

# Install PyAudio (Windows)
pip install PyAudio

# Install PyAudio (macOS)
brew install portaudio
pip install PyAudio

# Install PyAudio (Linux)
sudo apt-get install python3-pyaudio
```

#### **Voice Recognition Issues**
```bash
# Check Vosk model
ls models/vosk-model-small-en-us-0.15/

# Reinstall speech recognition
pip uninstall SpeechRecognition
pip install SpeechRecognition

# Test microphone access
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

#### **Streamlit Issues**
```bash
# Clear Streamlit cache
streamlit cache clear

# Check Streamlit version
streamlit --version

# Reinstall Streamlit
pip install --upgrade streamlit
```

### **Performance Optimization**

#### **For Better Recognition**
- Use a high-quality microphone
- Minimize background noise
- Speak clearly and at normal pace
- Ensure good internet connection (for Google SR)

#### **For Faster Response**
- Use offline Vosk model for basic commands
- Enable conversation mode for continuous interaction
- Customize wake word for easier activation

## 📱 Advanced Usage

### **Conversation Mode**
```bash
# Enable continuous listening
1. Click "🔄 Conversation Mode"
2. Say "Hey Assistant" to start
3. Give commands without repeating wake word
4. Say "Stop listening" to exit
```

### **Custom Wake Words**
```bash
# Change activation phrase
1. Click "⚙️ Settings"
2. Enter new wake word (e.g., "Computer")
3. Click "Update Wake Word"
4. Use new phrase to activate
```

### **Voice Preferences**
```bash
# Adjust speech settings
1. Open Settings panel
2. Adjust Speech Rate (100-300)
3. Adjust Volume (0.0-1.0)
4. Test with "🔊 Test Voice" button
```

## 🔌 Integration

### **Database Connection**
The assistant automatically integrates with your existing database connections:
- SQLite, PostgreSQL, MySQL support
- Automatic schema detection
- Query optimization suggestions
- Data visualization capabilities

### **API Integration**
Easily extend with external services:
- OpenAI GPT for advanced NLP
- Custom API endpoints
- Webhook notifications
- Third-party integrations

### **Custom Commands**
Add your own voice commands:
```python
# In enhanced_voice_assistant.py
def _handle_custom_command(self, command: str):
    if "my custom action" in command.lower():
        # Your custom logic here
        return {"action": "custom", "response": "Custom action executed!"}
```

## 🚀 Future Enhancements

### **Planned Features**
- **Multi-language Support**: Spanish, French, German, etc.
- **Voice Biometrics**: User identification by voice
- **Advanced NLP**: Better intent recognition and context
- **Mobile App**: iOS and Android companion apps
- **Cloud Integration**: AWS, Azure, Google Cloud support

### **AI Improvements**
- **Learning Capabilities**: Remember user preferences
- **Predictive Commands**: Suggest commands based on usage
- **Natural Conversations**: More human-like interactions
- **Emotion Recognition**: Detect user mood and respond accordingly

## 📚 API Reference

### **Main Classes**

#### **EnhancedVoiceAssistant**
```python
# Initialize
assistant = get_enhanced_assistant()

# Basic operations
assistant.speak("Hello world")
text, confidence = assistant.listen_for_command()
response = assistant.process_command("Show me data")

# Advanced features
assistant.start_conversation_mode()
assistant.set_wake_word("Computer")
```

#### **Voice Commands**
```python
# Database queries
"show me data from {table}"
"analyze {table} trends"
"create query for {condition}"

# System commands
"open {application}"
"search for {query}"
"launch {program}"
```

## 🤝 Contributing

### **Development Setup**
```bash
# Clone repository
git clone <your-repo>
cd nlp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements_voice.txt
pip install -r requirements-dev.txt  # If available

# Run tests
python -m pytest tests/
```

### **Code Style**
- Follow PEP 8 guidelines
- Add type hints for all functions
- Include comprehensive docstrings
- Write unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Vosk**: Offline speech recognition
- **Google Speech Recognition**: Online speech recognition
- **Streamlit**: Web application framework
- **pyttsx3**: Text-to-speech engine
- **OpenAI**: Natural language processing inspiration

## 📞 Support

### **Getting Help**
- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs and feature requests
- **Discussions**: Ask questions and share ideas
- **Examples**: Review the voice command examples

### **Community**
- Join our community discussions
- Share your custom voice commands
- Contribute improvements and features
- Help other users with setup and usage

---

**🎤 Ready to transform your voice into powerful commands? Start your AI Voice Assistant today!**
