import tkinter as tk #Se crea una ventana principal usando tkinter con un área de texto desplazable (ScrolledText) para mostrar mensajes y un botón para iniciar OVA.
from tkinter.scrolledtext import ScrolledText
import threading  #Se utiliza threading para ejecutar el método run_ova en un hilo separado, permitiendo que la interfaz gráfica permanezca receptiva.
import pyttsx3  # Libreria de convesion de voz a texto
import speech_recognition as sr #Libreria para reconocimiento de voz


class OVAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OVA Interface")
        
        self.text_area = ScrolledText(root, wrap=tk.WORD, width=50, height=20, font=("Arial", 12))
        self.text_area.pack(pady=10, padx=10)
        #Iniciar programa
        self.start_button = tk.Button(root, text="Iniciar OVA", command=self.initialize_ova)
        self.start_button.pack(pady=10)
        #Detener programa
        
        
        self.tts_engine = self.init_tts_engine()
        self.recognizer, self.microphone = self.init_recognizer()
        self.language = 'es'
        
    def init_tts_engine(self): #Se inicializan los motores TTS y de reconocimiento de voz, y se define el idioma inicial como español.
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1)
        return engine
    
    def speak(self, text): # Se determina las voces utilizadas según el lenguaje
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
            self.log_message("Escuchando...") #Los mensajes se muestran en el área de texto desplazable con este metodo
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        
        try: #Muestra los mensajes segun lo escuchado
            response = self.recognizer.recognize_google(audio, language='en-US' if self.language == 'en' else 'es-ES')
            self.log_message(f"Escuchaste: {response}")
            return response
        except sr.UnknownValueError:
            self.log_message("No se pudo entender el audio")
            return None
        except sr.RequestError: #Si no cuenta con conexion al servicio de reconocimiento de voz muestra este mensaje
            self.log_message("Error al comunicarse con el servicio de reconocimiento de voz")
            return None
        
    def ask_questions(self):
        if self.language == 'en':
            questions = [
                "What is your name?",
                "How old are you?",
                "What is your address?",
                "What is your phone number?",
                "What is your email address?"
            ]
        else:
            questions = [
                "¿Cuál es tu nombre?",
                "¿Cuál es tu edad?",
                "¿Cuál es tu dirección?",
                "¿Cuál es tu número de teléfono?",
                "¿Cuál es tu correo electrónico?"
            ]
        
        responses = {} #se guardan las respuestas en un diccionario
        
        for question in questions:
            self.speak(question)
            response = None
            while response is None:
                response = self.listen_for_response()
            responses[question] = response
            self.speak(f"I understand your {question.lower()} is {response}." if self.language == 'en'
                       else f"Entiendo que tu {question.lower()} es {response}.")
        
        self.log_message("Respuestas obtenidas: " + str(responses))
        
    def initialize_ova(self):
        threading.Thread(target=self.run_ova).start()
        
    def run_ova(self):
        self.log_message("<<<Inicializando Ova>>>")
        while True:
            self.log_message("Di 'Hola Ova' para comenzar.")
            response = self.listen_for_response()
            if response and 'hola ova' in response.lower():
                break
        
        while True:
            if self.language == 'es':
                self.log_message("Puedes cambiar el idioma diciendo 'Hello Ova' o 'Hi Ova'.")
            else:
                self.log_message("You can change the language by saying 'Hola Ova'.")
            
            response = self.listen_for_response()
            if response:
                if self.language == 'es' and ('hello ova' in response.lower() or 'hi ova' in response.lower()):
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
