# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame, random

pygame.init()

# ----- Gera tela principal
WIDTH = 600
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jogo de Empilhar Blocos')

# ----- Inicia estruturas de dados
img = pygame.image.load('bloco.png').convert()
BLOCO_WIDTH = 70
BLOCO_HEIGHT = 70

class Bloco(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = 0
        self.speedx = 5
        self.speedy = 0
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left > WIDTH:
            self.rect.x = -100
            self.rect.y = 0
            self.speedx = 5
            self.speedy = 0
        if self.rect.bottom == HEIGHT:
            self.speedx = 0
            self.speedy = 0
        
game = True
clock = pygame.time.Clock()
FPS = 60
bloco1 = Bloco(img)

# ===== Loop principal =====
while game:
    clock.tick(FPS)
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bloco1.speedx = 0
                bloco1.speedy = 5

        if event.type == pygame.QUIT:
            game = False
 
    bloco1.update()

    # ----- Gera saídas
    window.fill((255, 255, 255))  # Preenche com a cor branco
    window.blit(bloco1.image, bloco1.rect)

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados