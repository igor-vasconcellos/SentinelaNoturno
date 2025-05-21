import tkinter as tk
from tkinter import ttk, messagebox 
import threading  # cria a thread para tocar o alarme sem travar a interface
import time  # usado para contar o tempo de resposta
import csv  # salva as respostas em .csv
from os.path import exists
from datetime import datetime  # para registrar data e hora
import pygame  # para tocar o som de alerta
import yagmail  # para enviar e-mail com relatório
from PIL import Image, ImageTk  # exibe logo (necessário instalar o pillow)
import os

# lista de nomes válidos
operator = ["Glauber", "Igor", "Alex", "Léo"]
question = "Qual é o resultado de 14 - 5?"
correct_Answer = "9"
CSV_FILE = "relatorio_respostas.csv"
HORA_INICIO = 0
HORA_FIM = 6
INTERVALO_MIN = 15

dados_respostas = []  # armazena as respostas temporariamente

# toca um alarme em loop até alguém responder
def tocar_alarme_loop():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(".mp3")
        pygame.mixer.music.play(-1)  # -1 toca em loop
    except Exception as e:
        print(f"Erro ao tocar som: {e}")

# para o som do alarme
def parar_alarme():
    try:
        pygame.mixer.music.stop()
    except:
        pass

# salva os dados da resposta em uma lista
def registrar_resposta(monitor, resposta, tempo):
    agora = datetime.now()
    dados_respostas.append([
        agora.strftime("%Y-%m-%d"),
        agora.strftime("%H:%M:%S"),
        monitor,
        "Sim" if resposta else "Não",
        "Sim" if resposta == correct_Answer else "Não",
        f"{tempo:.1f}s" if tempo else "N/A"
    ])

# salva as respostas no arquivo csv
def salvar_csv():
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Data", "Hora", "Monitor", "Respondeu", "Resposta_Correta", "Tempo_Resposta"])
        writer.writerows(dados_respostas)

# envia o e-mail com o relatório anexado
def enviar_email():
    if not dados_respostas:
        print("Nenhum dado para enviar.")
        return
    try:
        print("Iniciando envio de e-mail...")
        yag = yagmail.SMTP(user="igor.santana.protector@gmail.com", password="oozgokjryocslpky")
        assunto = f"[Monitoramento Noturno] Relatório - {datetime.now().strftime('%d/%m/%Y')}"
        
        resumo_respostas = ""
        for item in dados_respostas:
            if len(item) >= 4:
                data, hora, nome, resposta = item[0], item[1], item[2], item[3]
                resumo_respostas += f"• Nome: {nome}, Resposta: {resposta}, Horário: {hora}\n"

        corpo_email = f"""
        Olá,

        Segue abaixo o relatório gerado automaticamente pelo sistema de monitoramento noturno em {datetime.now().strftime('%d/%m/%Y %H:%M')}.

        📋 Resumo das respostas capturadas:
        {resumo_respostas}

        O relatório completo está anexado em formato .csv.

        Atenciosamente,  
        Sistema Equipe Protector Serviços De Segurança
        """
        yag.send(
            to="igorlivassan@gmail.com",
            subject=assunto,
            contents=corpo_email,
            attachments=CSV_FILE
        )
        print("E-mail enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# cria a interface gráfica e lida com os eventos
def start_window():
    resposta = {"valor": None}
    tempo_inicio = time.time()

    # verifica se nome e resposta foram preenchidos
    def verificar_campos(*args):
        nome = combo.get()
        resposta_txt = entry_resposta.get().strip()
        if nome != "Selecione" and resposta_txt:
            botao_enviar.config(state="normal")
        else:
            botao_enviar.config(state="disabled")

    # envia os dados, salva e fecha a janela
    def enviar():
        parar_alarme()
        tempo = time.time() - tempo_inicio
        registrar_resposta(combo.get(), entry_resposta.get().strip(), tempo)
        salvar_csv()
        enviar_email()
        root.destroy()

    # caso o tempo acabe sem resposta
    def tempo_limite():
        if resposta["valor"] is None:
            parar_alarme()
            registrar_resposta(combo.get(), None, None)
            salvar_csv()
            enviar_email()
            root.destroy()

    # atualiza o tempo restante na tela
    def atualizar_timer():
        restante = int(60 - (time.time() - tempo_inicio))
        if restante >= 0:
            label_timer.config(text=f"⏳ Tempo restante: {restante} segundos")
            root.after(1000, atualizar_timer)

    # cria a janela principal
    root = tk.Tk()
    root.title("Sentinela Noturno")
    root.geometry("600x600")
    root.resizable(False, False) 
    root.eval('tk::PlaceWindow . center')

    # inicia o alarme
    threading.Thread(target=tocar_alarme_loop, daemon=True).start()

    try:
        imagem2 = Image.open("protectorLogo.png")
        imagem2.thumbnail((120, 100)) 
        logo_img2 = ImageTk.PhotoImage(imagem2)
        tk.Label(root, image=logo_img2).place(x=450, y=15)  
    except:
        print("Erro ao carregar 2 logo.")

    fonte_titulo = ("Arial", 16, "bold")
    fonte_entrada = ("Arial", 14, "bold")
    fonte_botao = ("Arial", 16, "bold")

    container = tk.Frame(root)
    container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    tk.Label(container, text="Selecione seu nome:", font=fonte_titulo).pack(pady=5)
    combo = ttk.Combobox(container, values=operator, font=fonte_entrada, width=25, state="readonly")
    combo.current(0)
    combo.pack()
    combo.bind("<<ComboboxSelected>>", verificar_campos)

    tk.Label(container, text=f"Pergunta: {question}", font=fonte_titulo).pack(pady=10)
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

start_window()