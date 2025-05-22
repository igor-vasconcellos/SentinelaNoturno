import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading, time
from datetime import datetime
from config import operator
from model.perguntas_model import choice_question
from model.dados_model import register_answer, save_csv
from controller.interface_controller import play_alarm_loop, stop_alarm
from controller.monitor_controller import send_email

def start_window():
    resposta = {"valor": None}
    tempo_inicio = time.time()
    pergunta_info = choice_question()
    pergunta = pergunta_info["pergunta"]
    resposta_correta = pergunta_info["resposta"]

    def verificar_campos(*args):
        if combo.get() != "Selecione" and entry_resposta.get().strip():
            botao_enviar.config(state="normal")
        else:
            botao_enviar.config(state="disabled")

    def enviar():
        stop_alarm()
        tempo = time.time() - tempo_inicio
        resposta_usuario = entry_resposta.get().strip()
        correta = resposta_usuario.lower() == resposta_correta.lower()
        register_answer(combo.get(), resposta_usuario, correta, tempo)
        save_csv()
        send_email()
        root.destroy()

    def tempo_limite():
        if resposta["valor"] is None:
            stop_alarm()
            register_answer(combo.get(), None, False, None)
            save_csv()
            send_email()
            root.destroy()

    def atualizar_timer():
        restante = int(60 - (time.time() - tempo_inicio))
        if restante >= 0:
            label_timer.config(text=f"⏳ Tempo restante: {restante} segundos")
            root.after(1000, atualizar_timer)

    root = tk.Tk()
    root.title("Sentinela Noturno")
    root.geometry("600x600")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')

    threading.Thread(target=play_alarm_loop, daemon=True).start()

    try:
        imagem2 = Image.open("assets/protectorLogo.png")
        imagem2.thumbnail((120, 100))
        logo_img2 = ImageTk.PhotoImage(imagem2)
        tk.Label(root, image=logo_img2).place(x=450, y=15)
    except:
        print("Erro ao carregar a logo.")

    fonte_titulo = ("Arial", 16, "bold")
    fonte_entrada = ("Arial", 14, "bold")
    fonte_botao = ("Arial", 16, "bold")

    container = tk.Frame(root)
    container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    tk.Label(container, text="Selecione seu nome:", font=fonte_titulo).pack(pady=5)
    combo = ttk.Combobox(container, values=operator, font=fonte_entrada, width=25, state="readonly")
    combo.set("Selecione")
    combo.pack()
    combo.bind("<<ComboboxSelected>>", verificar_campos)

    tk.Label(container, text=f"Pergunta: {pergunta}", font=fonte_titulo).pack(pady=10)
    entry_resposta = tk.Entry(container, font=fonte_entrada, width=20)
    entry_resposta.pack(pady=5)
    entry_resposta.bind("<KeyRelease>", verificar_campos)

    botao_enviar = tk.Button(container, text="✅ ENVIAR", font=fonte_botao, width=20, height=2, command=enviar, state="disabled")
    botao_enviar.pack(pady=20)

    label_timer = tk.Label(container, text="", font=("Arial", 14, "bold"), fg="red")
    label_timer.pack(pady=10)

    atualizar_timer()
    root.after(60000, tempo_limite)
    root.mainloop()
