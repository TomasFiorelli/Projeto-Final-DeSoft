import pygame
from config import WIDTH, HEIGHT, QUIT, GAME_INICIO, GAME_INFORMATIVO, GAME_SCREEN, GAME_OVER
from Telas_de_Inicio import game_inicio_screen, game_informativo_screen
from Funcao_Principal import game_screen
from Tela_Final import game_over_screen

pygame.init()
pygame.mixer.init()

#Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jogo de Empilhar Blocos')

state = GAME_INICIO
contador = 0

# Fluxo do jogo
while state != QUIT:
    if state == GAME_INICIO:
        state = game_inicio_screen(window)
    elif state == GAME_INFORMATIVO:
        state = game_informativo_screen(window)
    elif state == GAME_SCREEN:
        state, contador = game_screen(window)
    elif state == GAME_OVER:
        state = game_over_screen(window, contador)


# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados