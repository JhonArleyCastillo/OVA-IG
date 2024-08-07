from django.http import HttpResponse
from django.template import Template, context


def saludo(request): #primera vista
    
    doc_externo = open("C:/Users/gemac/OVA/templates/index.html")
    
    plt = Template(doc_externo.read())
    
    doc_externo.close()
    
    ctx = context()
    
    documento = plt.render(ctx)
    
    return HttpResponse(documento)

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import pyttsx3
import speech_recognition as sr
import threading
import requests
import queue

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

        self.message_queue = queue.Queue()
        self.root.after(100, self.process_queue)
        
        self.listen_lock = threading.Lock()

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
        with self.listen_lock:  # Ensure only one listen_for_response runs at a time
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
                "¿Deseas guardar tu usuario"
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
        self.send_data_to_api(responses)

    def send_data_to_api(self, data):
        try:
            response = requests.post('http://127.0.0.1:8000/api/ova/', json=data)
            self.log_message(f"Respuesta de la API: {response.json()}")
        except Exception as e:
            self.log_message(f"Error al enviar datos a la API: {e}")

    def toggle_ova(self):
        if not self.running:
            self.initialize_ova()
        else:
            self.terminate_ova()

    def initialize_ova(self):
        if not self.running:
            self.running = True
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
        self.log_message("<<<Inicializando Ova>>>")
        while True:
            self.log_message("Di 'Hola hola' para comenzar.")
            response = self.listen_for_response()
            if response and 'hola hola' in response.lower():
                break

        while self.running:
            if self.language == 'es':
                self.log_message("Puedes cambiar el idioma diciendo 'Hello hello' o 'Hi ova'.")
            else:
                self.log_message("You can change the language by saying 'Hola hola'.")

            response = self.listen_for_response()
            if response:
                if self.language == 'es' and ('hello hello' in response.lower() or 'hi ova' in response.lower()):
                    self.language = 'en'
                    self.speak("Language changed to English.")
                elif self.language == 'en' and 'hola hola' in response.lower():
                    self.language = 'es'
                    self.speak("Idioma cambiado a español.")
                else:
                    self.ask_questions()

    def log_message(self, message):
        self.message_queue.put(message)

    def process_queue(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()
            self.text_area.insert(tk.END, message + "\n")
            self.text_area.see(tk.END)
        self.root.after(100, self.process_queue)

if __name__ == "__main__":
    root = tk.Tk()
    app = OVAApp(root)
    root.mainloop()
