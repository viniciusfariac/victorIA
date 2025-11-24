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
import whisper # Biblioteca esta responsavél pela transcrição
from gtts import gTTS
import tempfile
import subprocess

load_dotenv()
CAMINHO_DB = "db_context"
groq_api_key = os.getenv("GROQ_API_KEY")

prompt_template = """"
Você é uma inteligência artificial chamada Victoria, especializada em:
1. Informações sobre o Colégio Victorino. 
2. Conceitos e aplicações de Computação Quântica.
3. Respostas claras, diretas e naturais para uso por voz.

BASE DE CONHECIMENTO:
{base_conhecimento}

INSTRUÇÕES GERAIS:
- Sempre responda com linguagem natural, como se estivesse conversando com um humano.
- Evite termos técnicos desnecessários quando não forem relevantes.
- Quando a pergunta envolver:
  a) Colégio Victorino → responda com base nos dados presentes na base de conhecimento.
  b) Computação Quântica → explique conceitos de forma simples, objetiva e aplicada.
  c) Qualquer outro tema → responda de forma segura e clara, mesmo que a base não tenha informações.
- Caso não exista informação específica na base de conhecimento, diga que não pode falar sobre esse assunto.
- Suas respostas devem ser curtas o suficiente para serem ouvidas, mas completas o bastante para esclarecer.
- Nunca invente fatos sobre o Colégio Victorino; use apenas a base.
- Não quebre o personagem: você é Victoria, uma IA educada, profissional e gentil.

AGORA RESPONDA A PERGUNTA DO USUÁRIO:

Pergunta:
{pergunta}
"""

def transcricao_audio():
  qualidade_audio = 16000 # taxa de amostragem em Hz, 16000 Hz é suficiente para voz e recomendado para modelos como o Whisper.
  duracao = 10 # duracao da gravação do áudio

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
  return resposta

def perguntar(pergunta):
  funcao_embedding = HuggingFaceEmbeddings(
      model_name="sentence-transformers/all-MiniLM-L6-v2"
  )

  db = Chroma(persist_directory=CAMINHO_DB, embedding_function=funcao_embedding)
  resultados = db.similarity_search_with_relevance_scores(pergunta)

  if len(resultados) == 0 or resultados[0][1] < 0.1:
    print("Sem informações relevantes")  
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

pergunta = transcricao_audio()
resposta_ia = perguntar(pergunta)
temp_file = texto_para_audio(resposta_ia)
tocar_audio(temp_file)