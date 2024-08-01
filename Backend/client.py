import pyaudio #Reconocer la entrada de interfaz de audio
import asyncio #Hacer llamadas asincronas atravez del socket
import webrtcvad #Detecta si es voz o no es
import websockets # Permite la conexión con el servidor de python

CHANNELS = 2                             # Se pueden capturar 2 canales mono o estereo, en este caso es mono
RATE = 16000                              # Número de muestras a tomar por segundo
FRAME_DURATION = 20                       #Estas 5 variables permiten setear el audio que va al servidor a través del cliente
FORMAT = pyaudio.paInt16                  # Tiempo de duración de cada frame
CHUNK = int(RATE / 1000) # Tipo de dato en que se guardaran los frame
INPUT_DEVICE = "microfono"
SERVER = "ws://localhost:8003/"

# Funcion de validacion de audio
vad = webrtcvad.Vad()
vad.set_mode(1)


class SpeechRecognitionCliente:
    def __init__(self):
        self.transcript = "" #Contiene toda la transcripcion que se obtine durante el evento asincrono
        self.audio = pyaudio.PyAudio()# Se declara la interfaz de audio
    
        self.getAudioInterface() #Encuentra el indice del microfono
        self.setStreamSettings() # Se setean los parametros
        
        asyncio.run(self.startStream())# Detona el evento de inicio de la funcion asincrona startStream
        
        self.stream.close() #Cerrar los stream
        self.audio.terminate() # Cerrar la interfaz de audio

    
    async def startStream(self): # Función asincrona
        async with websockets.connect(SERVER) as websocket:
            frames = b''
            try:
                while True:
                    frame = self.stream.read(CHUNK, exception_on_overflow=False)
                    if vad.is_speech(frame, RATE):
                        frames += frame
                    elif len(frames) > 1:
                        await websocket.send(frames)
                        frames = b''
                        
                        text = await websocket.recv() #Captura el dato transformado de audio a texto, lo puedo imprimir, contanarlo o tomarlo
                        self.transcript = f"{self.transcript} {text}" if len(text) > 1 else self.transcript
                        print(f"> {self.transcript}")
                        
                        
                        
            except KeyboardInterrupt:
                await websocket.close()
                print(f"\nWebcocket closed.")
            except websockets.exceptions.ConnectionClosedError:
                print(f"\nWebcocket closed.")
            except Exception:
                print(f"\nWebcocket closed.")
            finally:
                print('*'*50)
                print(f"\nTranscript: \n\n{self.transcript}\n")
        

    def setStreamSettings(self):
        self.stream = self.audio.open( #Apertura de conexion de pyaudio
            input_device_index=self.inputDevice,
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)
        

    def getAudioInterface(self):
        self.inputDevice = None
        numDevices = self.audio.get_host_api_info_by_index(0)("deviceCount") #Encuentra todos los dispositivos en nuestra maquina
        for index in range(numDevices):
            name = self.audio.get_device_info_by_host_api_device_index(0, index).get("name")
            if name == INPUT_DEVICE:
                self.inputDevice = index
                break
        
        if not self.inputDevice:
            raise ValueError(f"Audio device was not found under name: {INPUT_DEVICE}")

if __name__ == '__main__':
    s = SpeechRecognitionCliente()