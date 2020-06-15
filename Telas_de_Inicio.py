# ===== Funções de Início =====
# Tela Inicial e Regras

import pygame
from config import GAME_INFORMATIVO, GAME_SCREEN, QUIT

def game_inicio_screen(window):  # Define o que acontece na tela inicial
    while True:
        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    return GAME_INFORMATIVO
            if event.type == pygame.QUIT:
                return QUIT

        # Desenha a tela inicial
        inicio_foto = pygame.image.load('img/Foto inicio.png').convert()        
        window.fill((0, 0, 0))
        window.blit(inicio_foto,(0, 0))
        pygame.display.update()

def game_informativo_screen(window):  # Define o que acontece na tela informativa
    while True:
        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    return GAME_SCREEN
                if event.key == pygame.K_ESCAPE:
                    return QUIT
            if event.type == pygame.QUIT:
                return QUIT

        # Desenha a tela de regras
        informativo_foto = pygame.image.load('img/Foto informativo.png').convert()        
        window.fill((0, 0, 0))
        window.blit(informativo_foto,(0, 0))
        pygame.display.update()