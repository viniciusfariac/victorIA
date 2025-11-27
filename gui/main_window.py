# gui/main_window.py
import tkinter as tk
import threading
import numpy as np
import subprocess
import sys
import os

# Adiciona o diretório pai ao path para importar o main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa as funções do main.py
from main import transcricao_audio, perguntar, texto_para_audio

# Variáveis globais
esta_gravando = False
esta_falando = False
barras_amplitude = [0] * 20

def tocar_audio_com_espectro(caminho_audio: str):
    global esta_falando
    esta_falando = True
    subprocess.run([
        "ffplay",
        "-nodisp",
        "-autoexit",
        caminho_audio
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    esta_falando = False

def desenhar_espectro(canvas):
    global barras_amplitude, esta_falando
    
    canvas.delete("all")
    largura = canvas.winfo_width()
    altura = canvas.winfo_height()
    num_barras = len(barras_amplitude)
    largura_barra = largura / num_barras
    
    for i in range(num_barras):
        if esta_falando:
            barras_amplitude[i] = np.random.uniform(0.3, 1.0)
        else:
            barras_amplitude[i] *= 0.5
        
        altura_barra = barras_amplitude[i] * altura * 0.8
        x1 = i * largura_barra + 5
        y1 = altura / 2 - altura_barra / 2
        x2 = x1 + largura_barra - 10
        y2 = altura / 2 + altura_barra / 2
        
        cor = "#591769" if esta_falando else "#F7F7F7"
        canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="")
    
    canvas.after(50, lambda: desenhar_espectro(canvas))

def processar_audio(botao_falar, status_label):
    global esta_gravando
    
    try:
        botao_falar.config(state="disabled", text="...")
        status_label.config(text="Estou ouvindo, pode falar!")
        
        pergunta = transcricao_audio()
        status_label.config(text="Processando...")
        
        resposta_ia = perguntar(pergunta)
        status_label.config(text="Falando...")
        
        temp_file = texto_para_audio(resposta_ia)
        tocar_audio_com_espectro(temp_file)
        
        status_label.config(text=" ")
    except Exception as e:
        status_label.config(text=f"Erro: {str(e)}")
        print(f"Erro: {e}")
    finally:
        esta_gravando = False
        botao_falar.config(state="normal", text="Clique para falar")

def iniciar_gravacao(botao_falar, status_label):
    global esta_gravando
    if not esta_gravando:
        esta_gravando = True
        thread = threading.Thread(target=processar_audio, args=(botao_falar, status_label))
        thread.daemon = True
        thread.start()

def iniciar_interface():
    # Criar janela principal
    janela = tk.Tk()
    janela.title("VictorIA - Assistente Virtual")
    janela.state('zoomed')  
    janela.configure(bg="#111111")

    # Frame centralizado
    frame_central = tk.Frame(janela, bg="#1a1a1a")
    frame_central.place(relx=0.5, rely=0.5, anchor="center")

    # Titulo
    titulo = tk.Label(
        frame_central,
        text="VictorIA",
        font=("Arial", 42, "bold"),
        bg="#1a1a1a",
        fg="#591769"
    )
    titulo.pack(pady=40)

    # Canvas para espectro de áudio
    canvas_espectro = tk.Canvas(
        frame_central,
        width=600,
        height=250,
        bg="#0a0a0a",
        highlightthickness=0
    )
    canvas_espectro.pack(pady=40)

    # Label de status
    status_label = tk.Label(
        frame_central,
        text="Pronto para ouvir",
        font=("Arial", 14),
        bg="#1a1a1a",
        fg="#ffffff"
    )
    status_label.pack(pady=15)

    # Botão para falar
    botao_falar = tk.Button(
        frame_central,
        text="Clique para falar",
        font=("Arial", 16, "bold"),
        bg="#591769",
        fg="#000000",
        activebackground="#8100cc",
        activeforeground="#000000",
        command=lambda: iniciar_gravacao(botao_falar, status_label),
        cursor="hand2",
        padx=40,
        pady=20,
        relief="flat"
    )
    botao_falar.pack(pady=25)

    # Iniciar animação do espectro
    desenhar_espectro(canvas_espectro)

    # Iniciar interface
    janela.mainloop()

if __name__ == "__main__":
    iniciar_interface()