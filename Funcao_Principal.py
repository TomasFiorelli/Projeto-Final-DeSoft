import pygame
from config import BOTTOM, BOTTOM2, BLOCO_WIDTH, SPEED_CAM, HEIGHT, GAME_OVER, QUIT
from classe import Camera, Bloco

def game_screen(window):
    # Imagens e sons utilizados durante o loop principal
    img = pygame.image.load('img/predio_terreo.png').convert()
    foto_fundo = pygame.image.load('img/Foto fundo.png').convert()
    chao = pygame.image.load('img/chao.png').convert()
    foto_vida = pygame.image.load('img/vida.png').convert()
    som_plop = pygame.mixer.Sound('snd/som_plop.wav')

    game = True
    clock = pygame.time.Clock() # Variável para o ajuste de velocidade
    FPS = 60
    pos_chao = BOTTOM
    pos_fundo = BOTTOM2

    camera = Camera()

    ultimo_bloco_parado = None
    
    bloco = Bloco(img, BLOCO_WIDTH, camera)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bloco)
    all_blocks = pygame.sprite.Group()
    vidas = 3
    contador = 0
    
    # ===== Loop principal =====
    while game:
        clock.tick(FPS)
        
        # Verificação do bloco colocado (se precisa cortar ou não)
        hits = pygame.sprite.spritecollide(bloco, all_blocks, False)
        if bloco.rect.bottom == BOTTOM or len(hits) > 0:
            if contador == 0:
                if bloco.rect.bottom == BOTTOM:
                    som_plop.play()
                    contador +=1
            else:
                if bloco.rect.bottom == BOTTOM or bloco.rect.bottom > ultimo_bloco_parado.rect.centery: # Verifica se outro bloco, depois do primeiro, atingi o chão e mata ele
                    vidas -=1
                    bloco.kill()
                elif len(hits) > 0:
                    bloco_colisao = hits[0]
                    som_plop.play()
                    bloco.corta(bloco_colisao.rect.left, bloco_colisao.rect.right)
                    contador += 1
            
            if bloco.alive():
                bloco.speedx = 0
                bloco.speedy = 0
                ultimo_bloco_parado = bloco
                all_blocks.add(bloco)

            # Cria um novo bloco caso as vida seja diferente de 0
            largura = bloco.rect.width
            img = pygame.image.load('img/predio_andares.png').convert()
            bloco = Bloco(img, largura, camera)
            all_sprites.add(bloco)
        
        # A câmera segue o último bloco, fazendo com que a torre fique sempre no maximo no meio da tela
        if ultimo_bloco_parado is not None and ultimo_bloco_parado.rect.top <  HEIGHT / 2: 
            camera.speedy = SPEED_CAM
        else:
            camera.speedy = 0

        # Verificação de vidas
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
        
        # ----- Atualiza estado do jogo
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
        
        # Desenhando as vidas co uma imagem
        for i in range(vidas):
            window.blit(foto_vida, (525, 40 + i*45))
        
        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador