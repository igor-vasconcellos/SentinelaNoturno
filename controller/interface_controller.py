import pygame

def play_alarm_loop():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("assets/alarmes/alarme.mp3")
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Erro ao tocar som: {e}")

def stop_alarm():
    try:
        pygame.mixer.music.stop()
    except:
        pass