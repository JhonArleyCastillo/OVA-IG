# Realizar comparativa entre twice y ova7

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
        
        self.start_button = tk.Button(root, text="Iniciar OVA", command=self.toggle_ova)
        self.start_button.pack(pady=10)
        
        self.tts_engine = self.init_tts_engine()
        self.recognizer, self.microphone = self.init_recognizer()
        self.language = 'es'
        self.running = False
        self.stop_listening = None

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
                "¿Cuál es tu correo electrónico?",
                "¿Deseas guardar tu usuario?"
            ]
            
        responses = {}
        
        for question in questions:
            self.speak(question)
            response = None
            while response is None:
                response = self.listen_for_response()
            responses[question] = response
            self.speak(f"I understand your {question.lower()} is {response}." if self.language == 'en'
                       else f"Entiendo que tu respuesta a la pregunta {question.lower()} es {response}.")
        
        self.log_message("Respuestas obtenidas: " + str(responses))
        
    def toggle_ova(self):
        if not self.running:
            self.initialize_ova()
        else:
            self.terminate_ova()
        
    def initialize_ova(self):
        if not self.running:
            self.running = True
            self.start_button.config(text="Detener OVA")
            self.ova_thread = threading.Thread(target=self.run_ova)
            self.ova_thread.start()
        
    def terminate_ova(self):
        if self.running:
            self.running = False
            self.start_button.config(text="Iniciar OVA")
            self.log_message("OVA terminado.")
            self.tts_engine.stop()
            if self.stop_listening:
                self.stop_listening(wait_for_stop=False)
        
    def run_ova(self):
        self.log_message("<<<Inicializando OVA>>>")
        while not self.running:
            self.log_message("Di 'Hola hola' para comenzar.")
            response = self.listen_for_response()
            if response and 'hola hola' in response.lower():
                self.running = True
        
        def callback(recognizer, audio):
            try:
                response = recognizer.recognize_google(audio, language='en-US' if self.language == 'en' else 'es-ES')
                self.log_message(f"Escuchaste: {response}")
                if self.language == 'es' and ('hello hello' in response.lower() or 'hi ova' in response.lower()):
                    self.language = 'en'
                    self.speak("Language changed to English.")
                elif self.language == 'en' and 'hola hola' in response.lower():
                    self.language = 'es'
                    self.speak("Idioma cambiado a español.")
                else:
                    self.ask_questions()
            except sr.UnknownValueError:
                self.log_message("No se pudo entender el audio")
            except sr.RequestError:
                self.log_message("Error al comunicarse con el servicio de reconocimiento de voz")
        
        self.stop_listening = self.recognizer.listen_in_background(self.microphone, callback)
        
        while self.running:
            pass
        
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
        
    def log_message(self, message):
        self.text_area.after(0, self.text_area.insert, tk.END, message + "\n")
        self.text_area.after(0, self.text_area.see, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = OVAApp(root)
    root.mainloop()
