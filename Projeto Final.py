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
SPEED_CAM = 10

class Bloco(pygame.sprite.Sprite):
    def __init__(self, img, largura, camera):
        pygame.sprite.Sprite.__init__(self)
        
        img = pygame.transform.scale(img, (largura, BLOCO_HEIGHT))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = 0
        self.speedx = 5
        self.speedy = 0
        self.camera = camera
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy + self.camera.speedy
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
        
class Camera:
    def __init__(self):
        self.speedy = 0

game = True
clock = pygame.time.Clock()
FPS = 60

camera = Camera()

ultimo_bloco_parado = None
bloco = Bloco(img, BLOCO_WIDTH, camera)
all_sprites = pygame.sprite.Group()
all_sprites.add(bloco)
all_blocks = pygame.sprite.Group()
contador = 0
vidas =3

# ===== Loop principal =====
while game:
    clock.tick(FPS)
    
    hits = pygame.sprite.spritecollide(bloco, all_blocks, False)
    if bloco.rect.bottom == HEIGHT or len(hits) > 0:
        if contador == 0:
            if bloco.rect.bottom == HEIGHT:
                contador +=1
        else:
            if bloco.rect.bottom == HEIGHT:
                vidas -=1
                bloco.kill()
            if len(hits) > 0:
                bloco_colisao = hits[0]
                bloco.corta(bloco_colisao.rect.left, bloco_colisao.rect.right)
                contador += 1
            
        bloco.speedx = 0
        bloco.speedy = 0
        ultimo_bloco_parado = bloco
        all_blocks.add(bloco)
        largura = bloco.rect.width
        bloco = Bloco(img, largura, camera)
        all_sprites.add(bloco)
    
    if ultimo_bloco_parado is not None and ultimo_bloco_parado.rect.top <  HEIGHT / 2:
        camera.speedy = SPEED_CAM
    else:
        camera.speedy = 0

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
    
    # Desenhando o score
    text_surface = pygame.font.Font(None, 42).render("{:01d}".format(contador), True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (550,  10)
    window.blit(text_surface, text_rect)
    
    # Desenhando o vida
    text_surface = pygame.font.Font(None, 42).render("{:01d}".format(vidas), True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (550,  40)
    window.blit(text_surface, text_rect)
    

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
