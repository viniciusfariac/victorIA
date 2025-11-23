# Importando sounddevice
# Biblioteca esta responsavél pela captura do áudio do microfone
import sounddevice as sd
from scipy.io.wavfile import write

# Importando a biblioteca whisper
# Biblioteca esta responsavél pela transcrição
import whisper

# Configurando a gravação de áudio
qualidade_audio = 16000 # taxa de amostragem em Hz, 16000 Hz é suficiente para voz e recomendado para modelos como o Whisper.
duracao = 5 # duracao da gravação do áudio

print('Iniciando gravação!')
# Inicia a gravação do microfone e retorna uma lista onde o áudio será armazenado
audio = sd.rec(int(duracao * qualidade_audio), samplerate=qualidade_audio, channels=1)
# Espera até a gravação terminar
sd.wait()
print('Gravação concluida!')

# lista audio salva em um arquivo wav
write('gravacao.wav', qualidade_audio, audio)

# Escolhendo o modelo para realizar a transcrição
modelo = whisper.load_model("base")

# Armazenando o áudio que será transcrito
resposta = modelo.transcribe("gravacao.wav", language="pt", task="transcribe")

# Imprimindo transcrição
print('Transcrição realizada!!!')
print(resposta['text'])