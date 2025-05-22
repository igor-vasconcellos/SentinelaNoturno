import random

questions = [
    {"pergunta": "Qual é o resultado de 14 - 5?", "resposta": "9"},
    {"pergunta": "Escreva a palavra 'monitoramento'", "resposta": "monitoramento"},
    {"pergunta": "Quanto é 7 + 2?", "resposta": "9"},
    {"pergunta": "Qual é o resultado de 7 x 2?", "resposta": "14"},
    {"pergunta": "Quanto é 12 dividido por 4?", "resposta": "3"},
    {"pergunta": "Qual é a capital do Brasil?", "resposta": "Brasília"},
    {"pergunta": "Qual cor forma ao misturar azul e amarelo?", "resposta": "verde"},
    {"pergunta": "Quanto é 10 - 7?", "resposta": "3"},
    {"pergunta": "Quantos segundos tem 1 minuto?", "resposta": "60"},
    {"pergunta": "Escreva a palavra 'atenção'", "resposta": "atenção"},
    {"pergunta": "Quanto é 5 + 8?", "resposta": "13"},
    {"pergunta": "Escreva o número 21 por extenso:", "resposta": "vinte e um"},
    {"pergunta": "Qual é o resultado de 3 x 3?", "resposta": "9"},
    {"pergunta": "Qual é a capital da França?", "resposta": "Paris"},
    {"pergunta": "Quantos dias tem uma semana?", "resposta": "7"},
    {"pergunta": "Qual é o resultado de 15 - 6?", "resposta": "9"},
    {"pergunta": "Escreva a palavra 'proteção'", "resposta": "proteção"},
    {"pergunta": "Quanto é 4 + 5?", "resposta": "9"},
    {"pergunta": "Qual é o resultado de 8 dividido por 2?", "resposta": "4"},
    {"pergunta": "Quantas letras tem a palavra 'monitor'?", "resposta": "7"},
]

def choice_question():
    return random.choice(questions)
