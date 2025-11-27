# Victoria AI - Assistente Virtual Inteligente

**Victoria AI** é uma assistente virtual inteligente especializada em informações sobre o Colégio Victorino e Computação Quântica, com interface gráfica moderna e interação por voz.

---

## Índice

- [Características](#-características)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Como Usar](#-como-usar)
- [Interface Gráfica](#-interface-gráfica)
- [Arquitetura](#-arquitetura)
- [Solução de Problemas](#-solução-de-problemas)

---

## Características

- **Interação por Voz:** Fale diretamente com a assistente
- **Resposta em Áudio:** Respostas naturais convertidas em fala
- **Espectro de Áudio Animado:** Visualização em tempo real
- **Interface Moderna:** Design dark mode profissional
- **IA Avançada:** Powered by Groq e LangChain
- **Base de Conhecimento:** RAG com ChromaDB
- **Especializada:** Colégio Victorino + Computação Quântica

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+** - Linguagem principal
- **LangChain** - Framework para aplicações com LLM
- **Groq API** - Modelo de linguagem (GPT-OSS-20B)
- **ChromaDB** - Banco de dados vetorial
- **HuggingFace** - Embeddings (all-MiniLM-L6-v2)

### Processamento de Áudio
- **Whisper (OpenAI)** - Transcrição de voz para texto
- **gTTS** - Conversão de texto para fala
- **SoundDevice** - Gravação de áudio
- **FFmpeg/FFplay** - Reprodução de áudio

### Interface Gráfica
- **Tkinter** - GUI nativa do Python
- **NumPy** - Animação do espectro
- **Threading** - Processamento assíncrono

---

## 📁 Estrutura do Projeto

```
victoria-ai/
│
├── main.py                 # Lógica principal e funções core
├── .env                    # Configuração de variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo Git
├── README.md              # Este arquivo
│
├── gui/
│   └── main_window.py     # Interface gráfica Tkinter
│
├── db_context/            # Banco de dados vetorial (ChromaDB)
│   └── ...
│
└── requirements.txt       # Dependências do projeto
```

---

## Instalação

### Pré-requisitos

- Python 3.8 ou superior
- FFmpeg instalado no sistema
- Microfone funcional

### Passo 1: Clone o repositório

```bash
git clone https://github.com/seu-usuario/victoria-ai.git
cd victoria-ai
```

### Passo 2: Crie um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instale as dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Instale o FFmpeg

**Windows:**
1. Baixe em: https://ffmpeg.org/download.html
2. Adicione ao PATH do sistema

**Linux:**
```bash
sudo apt install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

---

## ⚙️ Configuração

### 1. Obtenha sua API Key do Groq

1. Acesse: https://console.groq.com/keys
2. Crie uma conta (grátis)
3. Gere uma nova API Key

### 2. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
# .env
GROQ_API_KEY=sua_api_key_aqui
```

**Exemplo:**
```env
GROQ_API_KEY=gsk_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
```

### 3. Prepare a base de conhecimento

Coloque seus arquivos PDF na pasta designada e execute:

```python
# Script de preparação da base (se necessário)
python preparar_base.py
```

---

##  Como Usar

### Executar a interface gráfica

```bash
python main.py
```

### Fluxo de uso

1. **Clique no botão** 🎤 "Clique para Falar"
2. **Fale sua pergunta** (10 segundos de gravação)
3. **Aguarde o processamento** (status aparece na tela)
4. **Ouça a resposta** (espectro anima durante a fala)
5. **Repita** quando quiser fazer outra pergunta

### Exemplos de perguntas

- "Quais são os horários do Colégio Victorino?"
- "Explique o que é computação quântica"
- "Como funcionam os qubits?"
- "Quais são as atividades extracurriculares do colégio?"

---

## 🎨 Interface Gráfica

### Design

A interface foi criada com **Tkinter** seguindo princípios de design moderno:

- **Dark Mode:** Fundo escuro (#1a1a1a) para conforto visual
- **Cores Vibrantes:** Roxo característico do colégio!(#591769) para elementos interativos
- **Centralização:** Todos os elementos centralizados na tela
- **Responsividade:** Tela maximizada automaticamente

### Componentes

#### 1. Título
```
VICTORIA AI
```
- Fonte: Arial 42pt Bold
- Cor: Roxo (#591769)

#### 2. Espectro de Áudio
```
████ ██ ████ ██ ████
```
- 20 barras animadas
- Animação: 20 FPS (50ms)
- Cores: Roxo (falando) / Branco (parado)

#### 3. Status
```
Gravando...
 Processando...
 Falando...
✓ Pronto!
```

#### 4. Botão Principal
```
[🎤 Clique para Falar]
```
- Tamanho: Grande e visível
- Estados: Normal / Hover / Disabled
- Cursor: Hand pointer

### Layout Visual

```
┌─────────────────────────────────────────┐
│         [TELA MAXIMIZADA]               │
│                                         │
│              VICTORIA AI                │
│                                         │
│       ████████████████████████          │
│                                         │
│          Pronto para ouvir              │
│                                         │
│       [🎤 Clique para Falar]            │
│                                         │
└─────────────────────────────────────────┘
```

---

##  Arquitetura

### Fluxo de Dados

```
┌──────────────┐
│   Usuário    │
│  (Microfone) │
└──────┬───────┘
       │
       ↓ (Áudio)
┌──────────────────┐
│    Whisper       │ ← Transcrição
│  (Speech-to-Text)│
└──────┬───────────┘
       │
       ↓ (Texto)
┌──────────────────┐
│   ChromaDB       │ ← Busca Vetorial
│  (RAG Search)    │
└──────┬───────────┘
       │
       ↓ (Contexto)
┌──────────────────┐
│   Groq API       │ ← Geração de Resposta
│   (LLM Model)    │
└──────┬───────────┘
       │
       ↓ (Texto)
┌──────────────────┐
│      gTTS        │ ← Síntese de Voz
│  (Text-to-Speech)│
└──────┬───────────┘
       │
       ↓ (Áudio)
┌──────────────────┐
│    FFplay        │ ← Reprodução
│   (Audio Player) │
└──────────────────┘
```

### Threading Model

```
┌─────────────────────┐
│   Main Thread       │ ← Interface Gráfica (UI)
│   (Tkinter Loop)    │
└──────────┬──────────┘
           │
           │ Cria
           ↓
┌─────────────────────┐
│   Worker Thread     │ ← Processamento de Áudio
│   (Audio Pipeline)  │
└─────────────────────┘
```

**Vantagens:**
- Interface não trava durante processamento
- Animação continua fluida
- Usuário tem feedback visual constante

---

##  Solução de Problemas

### Erro: "No module named 'tkinter'"

**Linux:**
```bash
sudo apt-get install python3-tk
```

**Mac:**
```bash
brew install python-tk
```

### Erro: "FFmpeg not found"

Certifique-se de que o FFmpeg está instalado e no PATH:

```bash
# Testar instalação
ffmpeg -version
ffplay -version
```

### Erro: "Permission denied" no microfone

**Windows:**
- Configurações → Privacidade → Microfone
- Permitir apps desktop

**Linux:**
```bash
sudo usermod -aG audio $USER
```

### Erro: "GROQ_API_KEY not found"

Verifique se o arquivo `.env` existe e está correto:

```bash
# Verificar conteúdo
cat .env

# Deve mostrar:
# GROQ_API_KEY=sua_chave_aqui
```

### Interface não centraliza

**Linux/Mac:** Descomente a linha alternativa em `gui/main_window.py`:

```python
# janela.state('zoomed')  # Comente esta
janela.attributes('-zoomed', True)  # Descomente esta
```

---

##  Notas Importantes

### Limitações

- Gravação limitada a **10 segundos**
- Requer conexão com internet (API Groq)
- Modelo Whisper "base" pode ter variações na precisão

### Melhorias Futuras

- [ ] Ajuste dinâmico do tempo de gravação
- [ ] Suporte para múltiplos idiomas
- [ ] Histórico de conversas
- [ ] Modo offline (modelo local)
- [ ] Customização de temas
- [ ] Atalhos de teclado

---

##  Desenvolvimento

### Estrutura de Código

**main.py** - Funções principais:
- `transcricao_audio()` - Grava e transcreve
- `perguntar()` - Processa com RAG + LLM
- `texto_para_audio()` - Converte resposta em áudio
- `tocar_audio()` - Reproduz o áudio

**gui/main_window.py** - Interface:
- `iniciar_interface()` - Cria a janela
- `desenhar_espectro()` - Anima as barras
- `processar_audio()` - Pipeline completo
- `iniciar_gravacao()` - Gerencia threading

### Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| `GROQ_API_KEY` | Chave da API Groq | ✅ Sim |

---

## 📄 Licença

Este projeto é de código aberto. Sinta-se livre para usar, modificar e distribuir.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no GitHub.

---

## 🎉 Agradecimentos

- **OpenAI** - Whisper
- **Anthropic** - Claude (documentação)
- **Groq** - API de LLM
- **LangChain** - Framework
- **Comunidade Python** - Bibliotecas open source

---

**Feito com ❤️ e ☕**

*Victoria AI - Assistente Virtual Inteligente*
