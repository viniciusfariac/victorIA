## Desenvolvimento...
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import sounddevice as sd
from scipy.io.wavfile import write
# Importando a biblioteca whisper
import whisper # Biblioteca esta responsavÃ©l pela transcriÃ§Ã£o
from gtts import gTTS
import tempfile
import subprocess

load_dotenv()
CAMINHO_DB = "db_context"
groq_api_key = os.getenv("GROQ_API_KEY")

prompt_template = """"
VocÃª Ã© uma inteligÃªncia artificial chamada Victoria, especializada em:
1. InformaÃ§Ãµes sobre o ColÃ©gio Victorino. 
2. Conceitos e aplicaÃ§Ãµes de ComputaÃ§Ã£o QuÃ¢ntica.
3. Respostas claras, diretas e naturais para uso por voz.
4. NUNCA USE ASTERISCOS, EMOJIS e CARACTERES ESPECIAIS
BASE DE CONHECIMENTO:
{base_conhecimento}

INSTRUÃ‡Ã•ES GERAIS:
- Sempre responda com linguagem natural, como se estivesse conversando com um humano.
- Evite termos tÃ©cnicos desnecessÃ¡rios quando nÃ£o forem relevantes.
- Quando a pergunta envolver:
  a) ColÃ©gio Victorino â†’ responda com base nos dados presentes na base de conhecimento.
  b) ComputaÃ§Ã£o QuÃ¢ntica â†’ explique conceitos de forma simples, objetiva e aplicada.
  c) Qualquer outro tema â†’ responda de forma segura e clara, mesmo que a base nÃ£o tenha informaÃ§Ãµes.
- Caso nÃ£o exista informaÃ§Ã£o especÃ­fica na base de conhecimento, diga que nÃ£o pode falar sobre esse assunto.
- Suas respostas devem ser curtas o suficiente para serem ouvidas, mas completas o bastante para esclarecer.
- Nunca invente fatos sobre o ColÃ©gio Victorino; use apenas a base.
- NÃ£o quebre o personagem: vocÃª Ã© Victoria, uma IA educada, profissional e gentil.

AGORA RESPONDA A PERGUNTA DO USUÃRIO:

Pergunta:
{pergunta}
"""

def transcricao_audio():
  qualidade_audio = 16000 # taxa de amostragem em Hz, 16000 Hz Ã© suficiente para voz e recomendado para modelos como o Whisper.
  duracao = 10 # duracao da gravaÃ§Ã£o do Ã¡udio

  print('Iniciando gravação!')
  # Inicia a gravaÃ§Ã£o do microfone e retorna uma lista onde o Ã¡udio serÃ¡ armazenado
  audio = sd.rec(int(duracao * qualidade_audio), samplerate=qualidade_audio, channels=1)
  # Espera atÃ© a gravaÃ§Ã£o terminar
  sd.wait()
  print('Gravação concluida!')

  # lista audio salva em um arquivo wav
  write('gravacao.wav', qualidade_audio, audio)

  # Escolhendo o modelo para realizar a transcriÃ§Ã£o
  modelo = whisper.load_model("base")

  # Armazenando o Ã¡udio que serÃ¡ transcrito
  resposta = modelo.transcribe("gravacao.wav", language="pt", task="transcribe")

  # Imprimindo transcriÃ§Ã£o
  print('Transcrição realizada!!!')
  print(resposta['text'])
  return resposta['text']

def perguntar(pergunta):
  funcao_embedding = HuggingFaceEmbeddings(
      model_name="sentence-transformers/all-MiniLM-L6-v2"
  )

  db = Chroma(persist_directory=CAMINHO_DB, embedding_function=funcao_embedding)
  resultados = db.similarity_search_with_relevance_scores(pergunta)

  if len(resultados) == 0 or resultados[0][1] < 0.1:
    print("Sem informaÃ§Ãµes relevantes")  
  # print(resultados, len(resultados))

  texto_resultados = []
  for resultado in resultados:
    texto = resultado[0].page_content
    texto_resultados.append(texto)
  base_conhecimento = "\n\n----\n\n".join(texto_resultados)
  prompt = ChatPromptTemplate.from_template(prompt_template)
  prompt = prompt.invoke({"pergunta": pergunta, "base_conhecimento": base_conhecimento})
  
  modelo = ChatGroq(
    groq_api_key=groq_api_key,
    model="openai/gpt-oss-20b",
    temperature=0.2
  )
  resposta = modelo.invoke(prompt)
  print(resposta.content)
  return resposta.content

def texto_para_audio(texto: str, idioma="pt") -> str:
    tts = gTTS(texto, lang=idioma)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name

def tocar_audio(caminho_audio: str):
    subprocess.run([
        "ffplay",
        "-nodisp",
        "-autoexit",
        caminho_audio
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# pergunta = transcricao_audio()
# resposta_ia = perguntar(pergunta)
# temp_file = texto_para_audio(resposta_ia)
# tocar_audio(temp_file)

if __name__ == "__main__":
    from gui.main_window import iniciar_interface
    iniciar_interface()

