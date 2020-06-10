# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame, random, time
from pygame.time import delay

pygame.init()

# ----- Gera tela principal
WIDTH = 600
HEIGHT = 800
BOTTOM = HEIGHT - 50
BOTTOM2 = - 2066
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jogo de Empilhar Blocos')

# ----- Inicia estruturas de dados
foto_fundo = pygame.image.load('/Users/gabriellazullo/Documents/Design de software/Projeto final/Foto fundo.png').convert()
BLOCO_WIDTH = 100
BLOCO_HEIGHT = 70
SPEED_CAM = 10
chao = pygame.image.load('/Users/gabriellazullo/Documents/Design de software/Projeto final/chao.png').convert()
foto_vida = pygame.image.load('/Users/gabriellazullo/Documents/Design de software/Projeto final/vida.png').convert ()

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

QUIT = 0
GAME_INICIO = 1
GAME_INFORMATIVO= 2
GAME_SCREEN = 3
GAME_OVER = 4

def game_inicio_screen(window):  #define o que acontece na tela inicial
    while True:
        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    return GAME_INFORMATIVO
            if event.type == pygame.QUIT:
                return QUIT
        inicio_foto = pygame.image.load('/Users/gabriellazullo/Documents/Design de software/Projeto final/Foto inicio.png').convert()        
        window.fill((0, 0, 0))
        window.blit(inicio_foto,(0, 0))
        pygame.display.update()

def game_informativo_screen(window):  #define o que acontece na tela informativa
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
        informativo_foto = pygame.image.load('/Users/gabriellazullo/Documents/Design de software/Projeto final/Foto informativo.png').convert()        
        window.fill((0, 0, 0))
        window.blit(informativo_foto,(0, 0))
        pygame.display.update()



def game_screen(window):
    game = True
    clock = pygame.time.Clock()
    FPS = 60
    pos_chao = BOTTOM
    pos_fundo = BOTTOM2

    camera = Camera()

    ultimo_bloco_parado = None
    img = pygame.image.load('/Users/gabriellazullo/Documents/Design de software/Projeto final/predio_terreo.png').convert()
    bloco = Bloco(img, BLOCO_WIDTH, camera)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bloco)
    all_blocks = pygame.sprite.Group()
    vidas = 3
    contador = 0
    # ===== Loop principal =====
    while game:
        clock.tick(FPS)
        
        hits = pygame.sprite.spritecollide(bloco, all_blocks, False)
        if bloco.rect.bottom == BOTTOM or len(hits) > 0:
            if contador == 0:
                if bloco.rect.bottom == BOTTOM:
                    contador +=1
            else:
                if bloco.rect.bottom == BOTTOM or bloco.rect.bottom > ultimo_bloco_parado.rect.centery: #verifica se outro bloco, depois do primeiro, atingi o chão e mata ele
                    vidas -=1
                    bloco.kill()
                elif len(hits) > 0:
                    bloco_colisao = hits[0]
                    bloco.corta(bloco_colisao.rect.left, bloco_colisao.rect.right)
                    contador += 1
            
            if bloco.alive():
                bloco.speedx = 0
                bloco.speedy = 0
                ultimo_bloco_parado = bloco
                all_blocks.add(bloco)
            largura = bloco.rect.width
            img = pygame.image.load('/Users/gabriellazullo/Documents/Design de software/Projeto final/predio_andares.png').convert()
            bloco = Bloco(img, largura, camera)
            all_sprites.add(bloco)
        
        if ultimo_bloco_parado is not None and ultimo_bloco_parado.rect.top <  HEIGHT / 2: #a camera segue o ultimo bloco, fazendo com que a torre fique sempre no maximo no meio da tela
            camera.speedy = SPEED_CAM
        else:
            camera.speedy = 0

        if vidas == 0:
            return GAME_OVER, contador

        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bloco.speedx = 0
                    bloco.speedy = 5

            if event.type == pygame.QUIT:
                return QUIT
            
        all_sprites.update()
        pos_chao += camera.speedy  # Atualiza posição do chão
        pos_fundo += camera.speedy

        # ----- Gera saídas
        window.fill((255, 255, 255))  # Preenche com a cor branco
        window.blit(foto_fundo,(0, pos_fundo))
        all_sprites.draw(window)
        window.blit(chao,(0, pos_chao))

        # Desenhando o score
        text_surface = pygame.font.Font(None, 42).render("{:01d}".format(contador), True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (550,  10)
        window.blit(text_surface, text_rect)
        
        # Desenhando o vida
        for i in range(vidas):
            window.blit(foto_vida, (525, 40 + i*45))
        
        #text_surface = pygame.font.Font(None, 42).render("{:01d}".format(vidas), True, (0, 0, 0))
        #text_rect = text_surface.get_rect()
        #text_rect.midtop = (550,  40)
        #window.blit(text_surface, text_rect)
        

        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador

def game_over_screen(window, contador):  #define o que acontece na tela final
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
                
        game_over_foto = pygame.image.load('/Users/gabriellazullo/Documents/Design de software/Projeto final/Foto final.png').convert()        
        font = pygame.font.SysFont(None, 80)
        if contador == 1:
            text2 = 'bloco'
        else:
            text2 = 'blocos'
        text1 = font.render('{}'.format(contador), True, (255, 255, 255))
        text2 = font.render('{}'.format(text2), True, (255, 255, 255))
        window.fill((0, 0, 0))
        window.blit(game_over_foto,(0, 0))
        
        window.blit(text1, (250, 425))
        window.blit(text2, (180, 475))
        pygame.display.update()


state = GAME_INICIO
contador = 0
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
