import pygame
from config import GAME_SCREEN, QUIT


def game_over_screen(window, contador): # Função que chama a tela final
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

        # Desenha uma imagem de fundo e escrve a pontuação final       
        game_over_foto = pygame.image.load('img/Foto final.png').convert()        
        
        if contador == 1:
            text2 = 'bloco'
        else:
            text2 = 'blocos'

        font = pygame.font.SysFont(None, 80)
        text1 = font.render('{}'.format(contador), True, (255, 255, 255))
        text2 = font.render('{}'.format(text2), True, (255, 255, 255))
        
        window.fill((0, 0, 0))
        window.blit(game_over_foto,(0, 0))
        window.blit(text1, (250, 425))
        window.blit(text2, (180, 475))
        
        pygame.display.update() 
