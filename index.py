import os
import requests
from gtts import gTTS
import tempfile
import subprocess

# ==========================================
# CONFIGURAÇÃO
# ==========================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("ERRO: Defina a variável de ambiente GROQ_API_KEY antes de usar o script.")


# ==========================================
# HISTÓRICO DA CONVERSA
# ==========================================

historico = [
    {"role": "system", "content": "Você é uma IA amigável. Mantenha a conversa coerente e lembre-se do histórico anterior."}
]


# ==========================================
# FUNÇÃO: Enviar texto para a API Groq (com memória)
# ==========================================

def gerar_resposta_groq(prompt: str) -> str:
    global historico

    # Adiciona a fala do usuário ao histórico
    historico.append({"role": "user", "content": prompt})

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}",
    }

    body = {
        "model": "openai/gpt-oss-20b",
        "messages": historico
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"Erro da API Groq: {response.text}")

    data = response.json()
    resposta = data["choices"][0]["message"]["content"]

    # Salva resposta da IA no histórico
    historico.append({"role": "assistant", "content": resposta})

    return resposta


# ==========================================
# TEXTO → ÁUDIO (gTTS)
# ==========================================

def texto_para_audio(texto: str, idioma="pt") -> str:
    tts = gTTS(texto, lang=idioma)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name


# ==========================================
# TOCAR ÁUDIO VIA FFPLAY
# ==========================================

def tocar_audio(caminho_audio: str):
    subprocess.run([
        "ffplay",
        "-nodisp",
        "-autoexit",
        caminho_audio
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ==========================================
# LOOP PRINCIPAL COM MEMÓRIA
# ==========================================

def main():
    print("IA iniciada! Digite 'sair' para encerrar.\n")

    while True:
        user_text = input("Você: ")

        if user_text.lower().strip() == "sair":
            print("Encerrando...")
            break

        print("\nIA está pensando...")
        resposta = gerar_resposta_groq(user_text)

        print("\nIA:", resposta)

        print("\nGerando áudio...")
        caminho_audio = texto_para_audio(resposta)

        print("Tocando resposta...")
        tocar_audio(caminho_audio)

        print("\n------------------------------------\n")


if __name__ == "__main__":
    main()