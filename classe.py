import pygame
from config import BLOCO_HEIGHT, WIDTH, HEIGHT

class Bloco(pygame.sprite.Sprite):
    def __init__(self, img, largura, camera):
        pygame.sprite.Sprite.__init__(self)
        
        img = pygame.transform.scale(img, (largura, BLOCO_HEIGHT))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = posicao_inicial[0]
        self.rect.y = posicao_inicial[1]
        self.speedx = 5
        self.speedy = 0
        self.camera = camera
        
    def verificaEscape (self):
        if self.rect.left > WIDTH:
            self.rect.x = posicao_inicial[0]
            self.rect.y = posicao_inicial[1]
            self.speedx = 5
            self.speedy = 0
    def verificaMorte (self):
        if self.rect.bottom == HEIGHT:
            self.speedx = 0
            self.speedy = 0

    def update(self):
        #atualização do movimento do bloco
        self.rect.x += self.speedx
        self.rect.y += self.speedy + self.camera.speedy
        verificaEscape(self)
        verificaMorte(self)
    
    def corta(self, esquerda, direita):
        #função que atualiza o bloco se ele for cortado, ou seja, quando o bloco é colocado errado em cima, corta e fica menor
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