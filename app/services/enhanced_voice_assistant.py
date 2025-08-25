import pyttsx3
import speech_recognition as sr
from typing import Optional, Tuple, Dict, List, Any
import time
import logging
import json
import queue
import sounddevice as sd
import numpy as np
import threading
import re
from datetime import datetime
import os
import tempfile
from vosk import Model, KaldiRecognizer
import webbrowser
import subprocess
import platform

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedVoiceAssistant:
    def __init__(self):
        """Initialize the enhanced voice assistant with multiple speech recognition engines."""
        self.conversation_history = []
        self.user_preferences = {}
        self.context = {}
        self.is_listening = False
        self.wake_word = "hey assistant"
        self.confidence_threshold = 0.7
        
        # Initialize text-to-speech engine
        self._init_tts()
        
        # Initialize speech recognition engines
        self._init_speech_recognition()
        
        # Initialize command patterns
        self._init_command_patterns()
        
        # Load user preferences
        self._load_user_preferences()

    def _init_tts(self):
        """Initialize text-to-speech engine with enhanced configuration."""
        try:
            self.engine = pyttsx3.init()
            
            # Enhanced TTS configuration
            self.engine.setProperty('rate', 160)      # Speed of speech
            self.engine.setProperty('volume', 0.9)    # Volume (0.0 to 1.0)
            
            # Get available voices and set a default
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to find a more natural-sounding voice
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                else:
                    self.engine.setProperty('voice', voices[0].id)
            
            logger.info("Text-to-speech engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None

    def _init_speech_recognition(self):
        """Initialize multiple speech recognition engines for fallback."""
        self.recognizers = {}
        
        # Initialize Vosk (offline)
        try:
            model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'models', 'vosk-model-small-en-us-0.15')
            if os.path.exists(model_path):
                self.recognizers['vosk'] = Model(model_path)
                logger.info("Vosk model loaded successfully")
            else:
                logger.warning("Vosk model not found, offline recognition disabled")
        except Exception as e:
            logger.warning(f"Failed to load Vosk model: {e}")
        
        # Initialize SpeechRecognition (online, requires internet)
        try:
            self.recognizers['sr'] = sr.Recognizer()
            self.recognizers['sr'].energy_threshold = 4000
            self.recognizers['sr'].dynamic_energy_threshold = True
            self.recognizers['sr'].pause_threshold = 0.8
            logger.info("SpeechRecognition initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize SpeechRecognition: {e}")

    def _init_command_patterns(self):
        """Initialize command patterns for natural language understanding."""
        self.command_patterns = {
            'database_query': [
                r'(show|display|get|find|search|query|analyze).*(data|table|database|records)',
                r'(how many|what is|tell me about).*(in|from|of).*(table|database)',
                r'(create|generate|write).*(sql|query).*(for|to)',
                r'(explain|describe).*(table|schema|structure)'
            ],
            'analysis_request': [
                r'(analyze|analyze|examine|investigate).*(data|trends|patterns)',
                r'(what are|show me|find).*(trends|patterns|insights)',
                r'(compare|contrast|difference between)',
                r'(statistics|summary|overview)'
            ],
            'system_command': [
                r'(open|launch|start).*(application|app|program)',
                r'(search|find|look up).*(on|in|for)',
                r'(set|change|modify).*(preference|setting)',
                r'(help|assist|support)'
            ],
            'conversation': [
                r'(hello|hi|hey|good morning|good afternoon|good evening)',
                r'(how are you|how do you do|what\'s up)',
                r'(thank you|thanks|appreciate)',
                r'(goodbye|bye|see you|farewell)'
            ]
        }

    def _load_user_preferences(self):
        """Load user preferences from file."""
        try:
            prefs_file = os.path.join(os.path.dirname(__file__), 'user_preferences.json')
            if os.path.exists(prefs_file):
                with open(prefs_file, 'r') as f:
                    self.user_preferences = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load user preferences: {e}")
            self.user_preferences = {}

    def speak(self, text: str, priority: bool = False) -> None:
        """Enhanced text-to-speech with priority handling."""
        if not self.engine:
            print(f"Speech output: {text}")
            return
        
        try:
            if priority:
                self.engine.stop()
            
            # Add natural pauses for better comprehension
            text = self._add_speech_pauses(text)
            
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Error in text-to-speech: {str(e)}")
            print(f"Speech output: {text}")

    def _add_speech_pauses(self, text: str) -> str:
        """Add natural pauses to speech for better comprehension."""
        # Add pauses after punctuation
        text = re.sub(r'([.!?])\s+', r'\1... ', text)
        # Add pauses before important conjunctions
        text = re.sub(r'\s+(but|however|therefore|meanwhile)\s+', r'... \1... ', text)
        return text

    def listen_for_command(self, timeout: int = 10, use_wake_word: bool = True) -> Tuple[Optional[str], float]:
        """Enhanced voice recognition with multiple engines and wake word detection."""
        if use_wake_word:
            # Listen for wake word first
            wake_detected = self._listen_for_wake_word(timeout=5)
            if not wake_detected:
                return None, 0.0
            
            self.speak("I'm listening. How can I help you?")
            time.sleep(0.5)
        
        # Try different recognition engines
        for engine_name, recognizer in self.recognizers.items():
            try:
                if engine_name == 'vosk':
                    text, confidence = self._recognize_with_vosk(recognizer, timeout)
                elif engine_name == 'sr':
                    text, confidence = self._recognize_with_sr(recognizer, timeout)
                else:
                    continue
                
                if text and confidence > self.confidence_threshold:
                    return text, confidence
                    
            except Exception as e:
                logger.warning(f"Recognition failed with {engine_name}: {e}")
                continue
        
        return None, 0.0

    def _listen_for_wake_word(self, timeout: int = 5) -> bool:
        """Listen for the wake word to activate the assistant."""
        try:
            if 'sr' in self.recognizers:
                return self._detect_wake_word_sr(timeout)
        except Exception as e:
            logger.error(f"Wake word detection failed: {e}")
        return False

    def _detect_wake_word_sr(self, timeout: int) -> bool:
        """Detect wake word using SpeechRecognition."""
        try:
            with sr.Microphone() as source:
                self.recognizers['sr'].adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizers['sr'].listen(source, timeout=timeout, phrase_time_limit=3)
                
                try:
                    text = self.recognizers['sr'].recognize_google(audio).lower()
                    return self.wake_word.lower() in text
                except sr.UnknownValueError:
                    return False
                except sr.RequestError:
                    return False
        except Exception as e:
            logger.error(f"SR wake word detection failed: {e}")
            return False

    def _recognize_with_vosk(self, model: Model, timeout: int) -> Tuple[Optional[str], float]:
        """Recognize speech using Vosk."""
        try:
            rec = KaldiRecognizer(model, 16000)
            rec.SetWords(True)
            
            audio_queue = queue.Queue()
            
            def audio_callback(indata, frames, time, status):
                if status:
                    logger.warning(f"Audio callback status: {status}")
                audio_queue.put(bytes(indata))
            
            with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
                start_time = time.time()
                text = ""
                
                while (time.time() - start_time) < timeout:
                    try:
                        data = audio_queue.get(timeout=0.1)
                        if rec.AcceptWaveform(data):
                            result = json.loads(rec.Result())
                            if result.get("text", "").strip():
                                text = result["text"]
                                break
                    except queue.Empty:
                        continue
                
                if not text:
                    final = json.loads(rec.FinalResult())
                    text = final.get("text", "").strip()
                
                # Estimate confidence based on text length and clarity
                confidence = min(0.9, len(text) / 50.0) if text else 0.0
                return text, confidence
                
        except Exception as e:
            logger.error(f"Vosk recognition failed: {e}")
            return None, 0.0

    def _recognize_with_sr(self, recognizer: sr.Recognizer, timeout: int) -> Tuple[Optional[str], float]:
        """Recognize speech using SpeechRecognition."""
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                try:
                    text = recognizer.recognize_google(audio)
                    # Google Speech API doesn't provide confidence scores, so we estimate
                    confidence = min(0.9, len(text) / 50.0) if text else 0.0
                    return text, confidence
                except sr.UnknownValueError:
                    return None, 0.0
                except sr.RequestError:
                    return None, 0.0
        except Exception as e:
            logger.error(f"SR recognition failed: {e}")
            return None, 0.0

    def process_command(self, command: str) -> Dict[str, Any]:
        """Process voice commands with natural language understanding and context awareness."""
        # Add to conversation history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': command,
            'assistant': None
        })
        
        # Analyze command intent
        intent = self._analyze_intent(command)
        
        # Generate response based on intent
        response = self._generate_response(command, intent)
        
        # Update conversation history
        self.conversation_history[-1]['assistant'] = response['response_text']
        
        # Update context
        self._update_context(command, intent, response)
        
        return response

    def _analyze_intent(self, command: str) -> Dict[str, Any]:
        """Analyze the intent of a voice command."""
        command_lower = command.lower()
        
        # Check command patterns
        for intent_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                if re.search(pattern, command_lower):
                    return {
                        'type': intent_type,
                        'confidence': 0.8,
                        'patterns_matched': [pattern]
                    }
        
        # Default to conversation intent
        return {
            'type': 'conversation',
            'confidence': 0.5,
            'patterns_matched': []
        }

    def _generate_response(self, command: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Generate appropriate response based on command intent."""
        intent_type = intent.get('type', 'conversation')
        
        if intent_type == 'database_query':
            return self._handle_database_query(command)
        elif intent_type == 'analysis_request':
            return self._handle_analysis_request(command)
        elif intent_type == 'system_command':
            return self._handle_system_command(command)
        elif intent_type == 'conversation':
            return self._handle_conversation(command)
        else:
            return self._handle_unknown_command(command)

    def _handle_database_query(self, command: str) -> Dict[str, Any]:
        """Handle database-related queries."""
        response_text = f"I understand you want to query the database. I'll help you with: {command}"
        
        return {
            'action': 'database_query',
            'response_text': response_text,
            'command': command,
            'data': {
                'query_type': 'database',
                'original_command': command
            }
        }

    def _handle_analysis_request(self, command: str) -> Dict[str, Any]:
        """Handle data analysis requests."""
        response_text = f"I'll help you analyze the data. You're asking about: {command}"
        
        return {
            'action': 'analysis_request',
            'response_text': response_text,
            'command': command,
            'data': {
                'query_type': 'analysis',
                'original_command': command
            }
        }

    def _handle_system_command(self, command: str) -> Dict[str, Any]:
        """Handle system-level commands."""
        command_lower = command.lower()
        
        if 'open' in command_lower or 'launch' in command_lower:
            return self._handle_application_launch(command)
        elif 'search' in command_lower:
            return self._handle_web_search(command)
        elif 'help' in command_lower:
            return self._handle_help_request(command)
        else:
            return {
                'action': 'system_command',
                'response_text': f"I'll help you with the system command: {command}",
                'command': command,
                'data': {'query_type': 'system'}
            }

    def _handle_application_launch(self, command: str) -> Dict[str, Any]:
        """Handle application launch requests."""
        # Extract application name from command
        app_patterns = [
            r'open\s+(.+?)(?:\s|$)',
            r'launch\s+(.+?)(?:\s|$)',
            r'start\s+(.+?)(?:\s|$)'
        ]
        
        app_name = None
        for pattern in app_patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                app_name = match.group(1).strip()
                break
        
        if app_name:
            try:
                # Try to launch the application
                if platform.system() == "Windows":
                    subprocess.Popen(['start', app_name], shell=True)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.Popen(['open', '-a', app_name])
                else:  # Linux
                    subprocess.Popen([app_name])
                
                response_text = f"I'm launching {app_name} for you."
                action = 'app_launched'
            except Exception as e:
                response_text = f"Sorry, I couldn't launch {app_name}. Error: {str(e)}"
                action = 'app_launch_failed'
        else:
            response_text = "I didn't catch which application you want me to open. Could you please specify?"
            action = 'unclear_command'
        
        return {
            'action': action,
            'response_text': response_text,
            'command': command,
            'data': {'app_name': app_name}
        }

    def _handle_web_search(self, command: str) -> Dict[str, Any]:
        """Handle web search requests."""
        search_patterns = [
            r'search\s+(?:for\s+)?(.+?)(?:\s|$)',
            r'find\s+(.+?)(?:\s|$)',
            r'look\s+up\s+(.+?)(?:\s|$)'
        ]
        
        search_query = None
        for pattern in search_patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                search_query = match.group(1).strip()
                break
        
        if search_query:
            try:
                search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                webbrowser.open(search_url)
                response_text = f"I'm searching the web for: {search_query}"
                action = 'web_search'
            except Exception as e:
                response_text = f"Sorry, I couldn't perform the web search. Error: {str(e)}"
                action = 'web_search_failed'
        else:
            response_text = "I didn't catch what you want me to search for. Could you please specify?"
            action = 'unclear_command'
        
        return {
            'action': action,
            'response_text': response_text,
            'command': command,
            'data': {'search_query': search_query}
        }

    def _handle_help_request(self, command: str) -> Dict[str, Any]:
        """Handle help requests."""
        help_text = """
        I'm your voice assistant! Here are some things I can help you with:
        
        • Database queries: "Show me the data", "Analyze this table"
        • Data analysis: "Find trends", "Compare results"
        • System commands: "Open calculator", "Search for Python tutorials"
        • General conversation: "Hello", "How are you"
        
        Just say "Hey Assistant" to wake me up, then tell me what you need!
        """
        
        return {
            'action': 'help_provided',
            'response_text': help_text,
            'command': command,
            'data': {'help_type': 'general'}
        }

    def _handle_conversation(self, command: str) -> Dict[str, Any]:
        """Handle general conversation."""
        command_lower = command.lower()
        
        if any(word in command_lower for word in ['hello', 'hi', 'hey']):
            response_text = "Hello! I'm your voice assistant. How can I help you today?"
        elif any(word in command_lower for word in ['how are you', 'how do you do']):
            response_text = "I'm doing well, thank you for asking! I'm ready to help you with any tasks."
        elif any(word in command_lower for word in ['thank you', 'thanks']):
            response_text = "You're welcome! I'm happy to help."
        elif any(word in command_lower for word in ['goodbye', 'bye', 'see you']):
            response_text = "Goodbye! Feel free to call me again if you need anything."
        else:
            response_text = f"That's interesting! You said: {command}. How can I assist you with that?"
        
        return {
            'action': 'conversation',
            'response_text': response_text,
            'command': command,
            'data': {'conversation_type': 'general'}
        }

    def _handle_unknown_command(self, command: str) -> Dict[str, Any]:
        """Handle commands that don't match known patterns."""
        response_text = f"I heard you say: {command}. I'm not sure how to help with that yet, but I'm learning! Could you try rephrasing or ask me for help to see what I can do?"
        
        return {
            'action': 'unknown_command',
            'response_text': response_text,
            'command': command,
            'data': {'query_type': 'unknown'}
        }

    def _update_context(self, command: str, intent: Dict[str, Any], response: Dict[str, Any]):
        """Update conversation context for better future interactions."""
        self.context.update({
            'last_command': command,
            'last_intent': intent,
            'last_action': response.get('action'),
            'timestamp': datetime.now().isoformat()
        })

    def start_conversation_mode(self) -> None:
        """Start continuous conversation mode."""
        self.is_listening = True
        self.speak("I'm now in conversation mode. Say 'Hey Assistant' to talk to me, or 'Stop listening' to exit.")
        
        while self.is_listening:
            try:
                command, confidence = self.listen_for_command(timeout=30, use_wake_word=True)
                
                if command:
                    if 'stop listening' in command.lower() or 'exit' in command.lower():
                        self.speak("Goodbye! I'm stopping conversation mode.")
                        self.is_listening = False
                        break
                    
                    # Process the command
                    response = self.process_command(command)
                    
                    # Speak the response
                    self.speak(response['response_text'])
                    
                    # Add a small pause for natural conversation flow
                    time.sleep(0.5)
                
            except KeyboardInterrupt:
                self.speak("Goodbye! I'm stopping conversation mode.")
                self.is_listening = False
                break
            except Exception as e:
                logger.error(f"Error in conversation mode: {e}")
                self.speak("I encountered an error. Let me try to continue listening.")

    def set_wake_word(self, new_wake_word: str) -> None:
        """Set a custom wake word."""
        self.wake_word = new_wake_word
        self.user_preferences['wake_word'] = new_wake_word
        self._save_user_preferences()
        self.speak(f"Wake word changed to: {new_wake_word}")

    def _save_user_preferences(self):
        """Save user preferences to file."""
        try:
            prefs_file = os.path.join(os.path.dirname(__file__), 'user_preferences.json')
            with open(prefs_file, 'w') as f:
                json.dump(self.user_preferences, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save user preferences: {e}")

# Create a singleton instance
enhanced_assistant_instance = None

def get_enhanced_assistant() -> EnhancedVoiceAssistant:
    """Get or create the enhanced voice assistant instance."""
    global enhanced_assistant_instance
    if enhanced_assistant_instance is None:
        enhanced_assistant_instance = EnhancedVoiceAssistant()
    return enhanced_assistant_instance
