import tkinter as tk
from tkinter import ttk, messagebox 
import threading # Para criar a interface gráfica
import time # Para manipulação de tempo
import csv # Para manipulação de arquivos CSV
from datetime import datetime, timedelta # Para manipulação de data e hora
import pygame # Para tocar o som de alerta
import yagmail # Para enviar email
from PIL import Image, ImageTk # certifique-se de ter 'Pillow' instalado
import tkinter as tk
from tkinter import ttk
import time
import os

MONITORES = ["Glauber", "Igor", "Alex", "Léo"]
PERGUNTA = "Qual é o resultado de 14 - 5?"
RESPOSTA_CORRETA = "9"
CSV_FILE = "relatorio_respostas.csv"
HORA_INICIO = 0
HORA_FIM = 6
INTERVALO_MIN = 15

dados_respostas = []


def tocar_alarme_loop():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("alarme.mp3")
        pygame.mixer.music.play(-1)  # Repetir até manualmente parar
    except Exception as e:
        print(f"Erro ao tocar som: {e}")

def parar_alarme():
    try:
        pygame.mixer.music.stop()
    except:
        pass

def registrar_resposta(monitor, resposta, tempo):
    agora = datetime.now()
    dados_respostas.append([
        agora.strftime("%Y-%m-%d"),
        agora.strftime("%H:%M:%S"),
        monitor,
        "Sim" if resposta else "Não",
        "Sim" if resposta == RESPOSTA_CORRETA else "Não",
        f"{tempo:.1f}s" if tempo else "N/A"
    ])

def salvar_csv():
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Data", "Hora", "Monitor", "Respondeu", "Resposta_Correta", "Tempo_Resposta"])
        writer.writerows(dados_respostas)

def enviar_email():
    if not dados_respostas:
        print("Nenhum dado para enviar.")
        return
    try:
        print("Iniciando envio de e-mail...")
        yag = yagmail.SMTP(user="igor.santana.protector@gmail.com", password="oozgokjryocslpky")
        print("Autenticado com sucesso.")
        assunto = f"Relatório de Monitoramento - {datetime.now().strftime('%Y-%m-%d')}"
        print(f"Assunto: {assunto}")
        yag.send(
            to="igorlivassan@gmail.com",
            subject=assunto,
            contents="Segue relatório em anexo.",
            attachments=CSV_FILE
        )
        print("E-mail enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


def iniciar_janela():
    resposta = {"valor": None}
    tempo_inicio = time.time()

    def verificar_campos(*args):
        nome = combo.get()
        resposta_txt = entry_resposta.get().strip()
        if nome != "Selecione" and resposta_txt:
            botao_enviar.config(state="normal")
        else:
            botao_enviar.config(state="disabled")

    def enviar():
        parar_alarme()
        tempo = time.time() - tempo_inicio
        registrar_resposta(combo.get(), entry_resposta.get().strip(), tempo)
        salvar_csv()
        enviar_email()
        root.destroy()

    def tempo_limite():
        if resposta["valor"] is None:
            parar_alarme()
            registrar_resposta(combo.get(), None, None)
            salvar_csv()
            enviar_email()
            root.destroy()

    def atualizar_timer():
        restante = int(60 - (time.time() - tempo_inicio))
        if restante >= 0:
            label_timer.config(text=f"⏳ Tempo restante: {restante} segundos")
            root.after(1000, atualizar_timer)

    root = tk.Tk()
    root.title("Confirmação do Monitor")
    root.geometry("600x600")
    root.eval('tk::PlaceWindow . center')

    # Tocar alarme em loop
    threading.Thread(target=tocar_alarme_loop, daemon=True).start()

    # LOGO
    try:
        imagem = Image.open("sentinelaNoturno.png")
        imagem = imagem.resize((120, 100))
        logo_img = ImageTk.PhotoImage(imagem)
        tk.Label(root, image=logo_img).place(x=10, y=10)
    except Exception as e:
        print("Erro ao carregar logo:", e)

    fonte_titulo = ("Arial", 16, "bold")
    fonte_entrada = ("Arial", 14, "bold")
    fonte_botao = ("Arial", 16, "bold")

    container = tk.Frame(root)
    container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    tk.Label(container, text="Selecione seu nome:", font=fonte_titulo).pack(pady=5)
    combo = ttk.Combobox(container, values=MONITORES, font=fonte_entrada, width=25, state="readonly")
    combo.current(0)
    combo.pack()
    combo.bind("<<ComboboxSelected>>", verificar_campos)

    tk.Label(container, text=f"Pergunta: {PERGUNTA}", font=fonte_titulo).pack(pady=10)
    entry_resposta = tk.Entry(container, font=fonte_entrada, width=20)
    entry_resposta.pack(pady=5)
    entry_resposta.bind("<KeyRelease>", verificar_campos)

    botao_enviar = tk.Button(container, text="✅ ENVIAR", font=fonte_botao, width=20, height=2, command=enviar, state="disabled")
    botao_enviar.pack(pady=20)

    label_timer = tk.Label(container, text="", font=("Arial", 14, "bold"), fg="red")
    label_timer.pack(pady=10)

    atualizar_timer()  # <- CHAMADA ADICIONADA AQUI!

    root.after(60000, tempo_limite)
    root.mainloop()


iniciar_janela()