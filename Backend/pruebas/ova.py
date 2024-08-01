import pyttsx3
import speech_recognition as sr

def init_tts_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    return engine

def speak(engine, text, language='es'):
    if language == 'en':
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')
    else:
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Monica')
    engine.say(text)
    engine.runAndWait()

def init_recognizer():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    return recognizer, microphone

def listen_for_response(recognizer, microphone, language='es'):
    with microphone as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        response = recognizer.recognize_google(audio, language='en-US' if language == 'en' else 'es-ES')
        print(f"Escuchaste: {response}")
        return response
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
        return None
    except sr.RequestError:
        print("Error al comunicarse con el servicio de reconocimiento de voz")
        return None

def ask_questions(engine, recognizer, microphone, language='es'):
    if language == 'en':
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
    
    responses = {}
    
    for question in questions:
        speak(engine, question, language)
        response = None
        while response is None:
            response = listen_for_response(recognizer, microphone, language)
        responses[question] = response
        speak(engine, f"I understand your {question.lower()} is {response}." if language == 'en'
              else f"Entiendo que tu {question.lower()} es {response}.", language)
    
    return responses

def initialize_ova(engine, recognizer, microphone):
    print("<<<Inicializando Ova>>>")
    while True:
        print("Di 'Hola cero' para comenzar.")
        response = listen_for_response(recognizer, microphone, 'es')
        if response and 'hola cero' in response.lower():
            break

    language = 'es'
    while True:
        if language == 'es':
            print("Puedes cambiar el idioma diciendo 'Hello cero' o 'Hi cero'.")
        else:
            print("You can change the language by saying 'Hola Ova'.")

        response = listen_for_response(recognizer, microphone, language)
        if response:
            if language == 'es' and ('hello cero' in response.lower() or 'hi cero' in response.lower()):
                language = 'en'
                speak(engine, "Language changed to English.", language)
            elif language == 'en' and 'hola ova' in response.lower():
                language = 'es'
                speak(engine, "Idioma cambiado a español.", language)
            else:
                responses = ask_questions(engine, recognizer, microphone, language)
                print("Respuestas obtenidas:", responses)

# Inicializar los motores
tts_engine = init_tts_engine()
recognizer, microphone = init_recognizer()

# Inicializar OVA y gestionar las preguntas
initialize_ova(tts_engine, recognizer, microphone)
