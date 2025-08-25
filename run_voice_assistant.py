#!/usr/bin/env python3
"""
Enhanced Voice Assistant Launcher
Run this script to start the AI Voice Assistant with full features.
"""

import os
import sys
import subprocess
import platform

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'plotly',
        'SpeechRecognition',
        'pyttsx3',
        'vosk',
        'sounddevice'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements_voice.txt")
        return False
    
    print("✅ All required packages are installed!")
    return True

def check_audio_devices():
    """Check if audio devices are available."""
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        print(f"🎵 Found {len(devices)} audio devices")
        return True
    except Exception as e:
        print(f"⚠️ Warning: Could not check audio devices: {e}")
        return False

def check_vosk_model():
    """Check if Vosk model is available."""
    model_path = os.path.join('models', 'vosk-model-small-en-us-0.15')
    if os.path.exists(model_path):
        print("✅ Vosk model found")
        return True
    else:
        print("⚠️ Vosk model not found. Downloading...")
        try:
            # Try to download the model
            subprocess.run([
                sys.executable, 
                'scripts/download_vosk_model.py'
            ], check=True)
            return True
        except Exception as e:
            print(f"❌ Failed to download Vosk model: {e}")
            print("📥 Please download manually from: https://alphacephei.com/vosk/models")
            return False

def main():
    """Main launcher function."""
    print("🎤 Enhanced Voice Assistant Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check audio devices
    check_audio_devices()
    
    # Check Vosk model
    if not check_vosk_model():
        print("\n⚠️ Voice recognition may not work without the Vosk model")
    
    print("\n🚀 Starting Enhanced Voice Assistant...")
    print("📱 The application will open in your default web browser")
    print("🎤 Say 'Hey Assistant' to activate voice commands")
    print("\n💡 Tips:")
    print("   - Use the 'Start Listening' button to begin")
    print("   - Try 'Conversation Mode' for continuous interaction")
    print("   - Check the examples in the app for voice command ideas")
    print("   - Press Ctrl+C in this terminal to stop the application")
    
    try:
        # Start the Streamlit app
        app_path = os.path.join('gui', 'enhanced_voice_app.py')
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', app_path,
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--browser.gatherUsageStats', 'false'
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Voice Assistant stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting Voice Assistant: {e}")
        print("🔧 Please check the error and try again")

if __name__ == "__main__":
    main()
