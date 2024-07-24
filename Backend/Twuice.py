import pyttsx3
import speech_recognition as sr

def init_tts_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    return engine

def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

def init_recognizer():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    return recognizer, microphone

def listen_for_response(recognizer, microphone):
    with microphone as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        response = recognizer.recognize_google(audio, language='es-ES')
        print(f"Escuchaste: {response}")
        return response
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
        return None
    except sr.RequestError:
        print("Error al comunicarse con el servicio de reconocimiento de voz")
        return None

def ask_questions(engine, recognizer, microphone):
    questions = [
        "¿Cuál es tu nombre?",
        "¿Cuál es tu edad?",
        "¿Cuál es tu dirección?",
        "¿Cuál es tu número de teléfono?",
        "¿Cuál es tu correo electrónico?"
    ]
    
    responses = {}
    
    for question in questions:
        speak(engine, question)
        response = None
        while response is None:
            response = listen_for_response(recognizer, microphone)
        responses[question] = response
        speak(engine, f"Entiendo que tu {question.lower()} es {response}.")
    
    return responses

# Inicializar los motores
tts_engine = init_tts_engine()
recognizer, microphone = init_recognizer()

# Hacer preguntas y obtener respuestas
responses = ask_questions(tts_engine, recognizer, microphone)
print("Respuestas obtenidas:", responses)
