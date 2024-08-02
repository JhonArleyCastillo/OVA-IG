import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import pyttsx3
import speech_recognition as sr

class OVAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OVA Interface")
        
        self.text_area = ScrolledText(root, wrap=tk.WORD, width=50, height=20, font=("Arial", 12))
        self.text_area.pack(pady=10, padx=10)
        
        self.start_button = tk.Button(root, text="Iniciar OVA", command=self.initialize_ova)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Terminar OVA", command=self.terminate_ova)
        self.stop_button.pack(pady=10)
        
        self.tts_engine = self.init_tts_engine()
        self.recognizer, self.microphone = self.init_recognizer()
        self.language = 'es'
        self.running = False
        
    def init_tts_engine(self):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1)
        return engine
    
    def speak(self, text):
        if self.language == 'en':
            self.tts_engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')
        else:
            self.tts_engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Monica')
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
        
    def init_recognizer(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        return recognizer, microphone
    
    def listen_for_response(self):
        with self.microphone as source:
            self.log_message("Escuchando...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        
        try:
            response = self.recognizer.recognize_google(audio, language='en-US' if self.language == 'en' else 'es-ES')
            self.log_message(f"Escuchaste: {response}")
            return response
        except sr.UnknownValueError:
            self.log_message("No se pudo entender el audio")
            return None
        except sr.RequestError:
            self.log_message("Error al comunicarse con el servicio de reconocimiento de voz")
            return None
        
    def ask_questions(self):
        if self.language == 'en':
            questions = [
                "What's your name?",
                "How old are you?",
                "What's your address?",
                "What's your phone number?",
                "What's your email address?"
            ]
        else:
            questions = [
                "¿Cuál es tu nombre?",
                "¿Cuál es tu edad?",
                "¿Cuál es tu dirección?",
                "¿Cuál es tu número de teléfono?",
                "¿Cuál es tu correo electrónico?"
            ]
        
        responses = {}
        
        for question in questions:
            self.speak(question)
            response = None
            while response is None:
                if not self.running:
                    return
                response = self.listen_for_response()
            responses[question] = response
            self.speak(f"I understand your {question.lower()} is {response}." if self.language == 'en'
                       else f"Entiendo que tu {question.lower()} es {response}.")
        
        self.log_message("Respuestas obtenidas: " + str(responses))
        
    def initialize_ova(self):
        self.running = True
        threading.Thread(target=self.run_ova).start()
        
    def terminate_ova(self):
        self.running = False
        self.log_message("OVA terminado.")
        
    def run_ova(self):
        self.log_message("<<<Inicializando Ova>>>")
        while self.running:
            self.log_message("Di 'Hola hola' para comenzar.")
            response = self.listen_for_response()
            if response and 'hola hola' in response.lower():
                break
        
        while self.running:
            if self.language == 'es':
                self.log_message("Puedes cambiar el idioma diciendo 'Hello ova' o 'Hi Ova'.")
            else:
                self.log_message("You can change the language by saying 'Hola Ova'.")
            
            response = self.listen_for_response()
            if response:
                if self.language == 'es' and ('hello' in response.lower() or 'hi ova' in response.lower()):
                    self.language = 'en'
                    self.speak("Language changed to English.")
                elif self.language == 'en' and 'hola ova' in response.lower():
                    self.language = 'es'
                    self.speak("Idioma cambiado a español.")
                else:
                    self.ask_questions()
                    
    def log_message(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = OVAApp(root)
    root.mainloop()
## sigue funcionando aun con el boton terminar programa, actualizacion fallida
