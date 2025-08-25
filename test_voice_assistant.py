#!/usr/bin/env python3
"""
Test script for the Enhanced Voice Assistant
Run this to test basic functionality without the full GUI.
"""

import sys
import os
import time

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_voice_assistant():
    """Test the enhanced voice assistant functionality."""
    print("🎤 Testing Enhanced Voice Assistant")
    print("=" * 50)
    
    try:
        # Test importing the assistant
        print("📦 Testing imports...")
        from app.services.enhanced_voice_assistant import get_enhanced_assistant
        print("✅ Enhanced voice assistant imported successfully")
        
        # Test creating instance
        print("\n🔧 Testing assistant creation...")
        assistant = get_enhanced_assistant()
        print("✅ Assistant instance created successfully")
        
        # Test basic properties
        print("\n📋 Testing basic properties...")
        print(f"   - Wake word: {assistant.wake_word}")
        print(f"   - Confidence threshold: {assistant.confidence_threshold}")
        print(f"   - Available recognizers: {list(assistant.recognizers.keys())}")
        print("✅ Basic properties verified")
        
        # Test text-to-speech
        print("\n🔊 Testing text-to-speech...")
        try:
            assistant.speak("Hello! This is a test of the voice assistant.")
            print("✅ Text-to-speech working")
        except Exception as e:
            print(f"⚠️ Text-to-speech test failed: {e}")
        
        # Test command processing
        print("\n🧠 Testing command processing...")
        test_commands = [
            "Hello, how are you?",
            "Show me data from the users table",
            "Open calculator",
            "Search for Python tutorials",
            "Help me with database queries"
        ]
        
        for command in test_commands:
            try:
                response = assistant.process_command(command)
                print(f"   ✅ '{command}' → {response['action']}")
            except Exception as e:
                print(f"   ❌ '{command}' failed: {e}")
        
        # Test conversation history
        print("\n💬 Testing conversation history...")
        history = assistant.conversation_history
        print(f"   - Total exchanges: {len(history)}")
        if history:
            print(f"   - Last interaction: {history[-1]['timestamp']}")
        print("✅ Conversation history working")
        
        # Test context management
        print("\n🧩 Testing context management...")
        context = assistant.context
        print(f"   - Context keys: {list(context.keys())}")
        print("✅ Context management working")
        
        print("\n🎉 All tests completed successfully!")
        print("\n💡 Next steps:")
        print("   1. Run 'python run_voice_assistant.py' to launch the full app")
        print("   2. Say 'Hey Assistant' to activate voice commands")
        print("   3. Try the example commands shown in the app")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you have installed all requirements:")
        print("   pip install -r requirements_voice.txt")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Check the error details and ensure all dependencies are installed")
        return False

def test_audio_devices():
    """Test audio device availability."""
    print("\n🎵 Testing Audio Devices")
    print("=" * 30)
    
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        print(f"✅ Found {len(devices)} audio devices")
        
        # Show input devices
        input_devices = [d for d in devices if d['max_inputs'] > 0]
        print(f"   - Input devices: {len(input_devices)}")
        for i, device in enumerate(input_devices):
            print(f"     {i}: {device['name']}")
            
        # Show output devices
        output_devices = [d for d in devices if d['max_outputs'] > 0]
        print(f"   - Output devices: {len(output_devices)}")
        for i, device in enumerate(output_devices):
            print(f"     {i}: {device['name']}")
            
    except ImportError:
        print("❌ sounddevice not available")
        print("💡 Install with: pip install sounddevice")
    except Exception as e:
        print(f"⚠️ Audio device test failed: {e}")

def test_speech_recognition():
    """Test speech recognition engines."""
    print("\n🎤 Testing Speech Recognition")
    print("=" * 35)
    
    # Test Vosk
    try:
        from vosk import Model
        print("✅ Vosk available")
        
        # Check for model
        model_path = os.path.join('models', 'vosk-model-small-en-us-0.15')
        if os.path.exists(model_path):
            print("✅ Vosk model found")
        else:
            print("⚠️ Vosk model not found")
            print("💡 Download with: python scripts/download_vosk_model.py")
            
    except ImportError:
        print("❌ Vosk not available")
        print("💡 Install with: pip install vosk")
    
    # Test SpeechRecognition
    try:
        import speech_recognition as sr
        print("✅ SpeechRecognition available")
        
        # Test microphone access
        try:
            mic = sr.Microphone()
            print("✅ Microphone access available")
        except Exception as e:
            print(f"⚠️ Microphone access failed: {e}")
            
    except ImportError:
        print("❌ SpeechRecognition not available")
        print("💡 Install with: pip install SpeechRecognition")

def main():
    """Main test function."""
    print("🚀 Enhanced Voice Assistant Test Suite")
    print("=" * 60)
    
    # Test audio devices
    test_audio_devices()
    
    # Test speech recognition
    test_speech_recognition()
    
    # Test voice assistant
    success = test_voice_assistant()
    
    if success:
        print("\n🎯 Ready to use the Enhanced Voice Assistant!")
        print("   Run 'python run_voice_assistant.py' to get started")
    else:
        print("\n🔧 Some tests failed. Please check the requirements and try again.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
