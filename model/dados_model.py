import csv
from datetime import datetime
from config import csv_file

data_answers = []

def register_answer(monitor, resposta, correta, tempo):
    agora = datetime.now()
    data_answers.append([
        agora.strftime("%Y-%m-%d"),
        agora.strftime("%H:%M:%S"),
        monitor,
        "Sim" if resposta else "Não",
        "Sim" if correta else "Não",
        f"{tempo:.1f}s" if tempo else "N/A"
    ])

def save_csv():
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Data", "Hora", "Monitor", "Respondeu", "Resposta_Correta", "Tempo_Resposta"])
        writer.writerows(data_answers)