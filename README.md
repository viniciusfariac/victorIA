# VictorIA – Assistente Virtual por Voz 🎤🤖

VictorIA é uma inteligência artificial de voz criada especialmente para a **Feira Cultural do Colégio Victorino**, capaz de **ouvir**, **interpretar**, **responder** e **falar** de forma natural.  
Ela combina tecnologias modernas de IA, processamento de áudio e interfaces interativas para oferecer uma experiência fluida ao usuário.

---

## 🧠 Sobre a VictorIA
VictorIA foi projetada para responder de forma **curta, objetiva e natural**, com foco em:

- Informações sobre o **Colégio Victorino**  
- Explicações simples de **Computação Quântica**  
- Perguntas gerais, sempre mantendo respostas diretas para uso por voz 

A IA também conta com uma base vetorizada de PDFs, garantindo que as respostas sobre o colégio sejam precisas e provenientes da documentação oficial.

---

## 🚀 Tecnologias Utilizadas

### **IA e Processamento de Linguagem**
- **LangChain** (prompts, embeddings e RAG)
- **Groq LLM (openai/gpt-oss-20b)** via `ChatGroq`
- **HuggingFace Embeddings** (sentence-transformers/all-MiniLM-L6-v2)
- **Whisper** (transcrição de áudio)

### **Processamento e Reprodução de Áudio**
- `sounddevice` (gravação do microfone)
- `scipy` (salvar arquivo wav)
- **Edge TTS** (geração de voz neural)
- `ffplay` (reprodução de áudio)

### **Interface Gráfica**
- **Tkinter**

### **Base de Conhecimento**
- PDFs transformados em chunks usando:
  - `PyPDFDirectoryLoader`
  - `RecursiveCharacterTextSplitter`
  - Banco vetorial **ChromaDB**

---

## ▶️ Como Executar o Projeto

### 1. Clone o repositório
```bash
git clone https://github.com/viniciusfariac/victorIA
cd victorIA
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python create_db.py
python main.py
```

## 🎧 Como funciona a interação

- O usuário clica no botão "Clique para falar"
- A IA grava 5 segundos de áudio
- O Whisper transcreve a fala
- A pergunta é enviada ao modelo Groq junto com a base vetorizada
- VictorIA gera a resposta e converte para áudio neural via Edge TTS
- O áudio é reproduzido enquanto um espectro animado aparece na tela