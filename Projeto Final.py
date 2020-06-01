# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame, random, time
from pygame.time import delay

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
    def __init__(self, img, largura):
        pygame.sprite.Sprite.__init__(self)
        
        img = pygame.transform.scale(img, (largura, BLOCO_HEIGHT))
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
    
    def corta(self, esquerda, direita):
        left = max(esquerda, self.rect.left)
        right = min(direita, self.rect.right)
        y = self.rect.y
        self.image = pygame.transform.scale(self.image, (right - left, BLOCO_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = left
        self.rect.y = y
        
game = True
clock = pygame.time.Clock()
FPS = 60

bloco = Bloco(img, BLOCO_WIDTH)
all_sprites = pygame.sprite.Group()
all_sprites.add(bloco)
all_blocks = pygame.sprite.Group()

# ===== Loop principal =====
while game:
    clock.tick(FPS)
    
    hits = pygame.sprite.spritecollide(bloco, all_blocks, False)
    if bloco.rect.bottom == HEIGHT or len(hits) > 0:
        if len(hits) > 0:
            bloco_colisao = hits[0]
            bloco.corta(bloco_colisao.rect.left, bloco_colisao.rect.right)
        bloco.speedx = 0
        bloco.speedy = 0
        all_blocks.add(bloco)
        largura = bloco.rect.width
        bloco = Bloco(img, largura)
        all_sprites.add(bloco)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bloco.speedx = 0
                bloco.speedy = 5

        if event.type == pygame.QUIT:
            game = False
 
    all_sprites.update()

    # ----- Gera saídas
    window.fill((255, 255, 255))  # Preenche com a cor branco
    all_sprites.draw(window)
    

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
