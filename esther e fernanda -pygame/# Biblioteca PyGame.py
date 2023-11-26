# Biblioteca PyGame
import pygame
# Biblioteca para geracao de numeros pseudoaleatorios
import random
# Modulo da biblioteca PyGame que permite o acesso as teclas utilizadas
from pygame.locals import *

# Classe que representar o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25)) #Define o retangulo que representa o player
        self.surf.fill((255, 255, 255)) #Preenche o retangulo com branco (RGB)
        self.rect = self.surf.get_rect()

    # Determina acao de movimento conforme teclas pressionadas
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Mantem o jogador nos limites da tela do jogo
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

# Classe que representa os inimigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10)) #Definicao do retangulo
        self.surf.fill((255,255,255)) #Preenche com cor branca (RGB)
        self.rect = self.surf.get_rect( #Coloca na extrema direita (entre 820 e 900) e sorteia sua posicao em relacao a coordenada y (entre 0 e 600)
            center=(random.randint(820, 900), random.randint(0, 600))
        )
        self.speed = random.uniform(1, 15) #Sorteia sua velocidade, entre 1 e 15

    # Funcao que atualiza a posiçao do inimigo em funcao da sua velocidade e termina com ele quando ele atinge o limite esquerdo da tela (x < 0)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Inicializa pygame
pygame.init()

# Cria a tela com resolução 800x600px
screen = pygame.display.set_mode((800, 600))

# Cria um evento para adicao de inimigos
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250) #Define um intervalo para a criacao de cada inimigo (milisegundos)

# Cria o jogador (nosso retangulo)
player = Player()

# Define o plano de fundo, com a cor preta (RGB)
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))

enemies = pygame.sprite.Group() #Cria o grupo de inimigos
all_sprites = pygame.sprite.Group() #Cria o grupo de todos os Sprites
all_sprites.add(player) #Adicionar o player no grupo de todos os Sprites

running = True #Flag para controle do jogo

while running:
    #Laco para verificacao do evento que ocorreu
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: #Verifica se a tecla ESC foi pressionada
                running = False
        elif event.type == QUIT: #Verifica se a janela foi fechada
            running = False
        elif(event.type == ADDENEMY): #Verifica se e o evento de criar um inimigo
            new_enemy = Enemy() #Cria um novo inimigo
            enemies.add(new_enemy) #Adiciona o inimigo no grupo de inimigos
            all_sprites.add(new_enemy) #Adiciona o inimigo no grupo de todos os Sprites
    screen.blit(background, (0, 0)) #Atualiza a exibicao do plano de fundo do jogo (neste caso nao surte efeito)
    pressed_keys = pygame.key.get_pressed() #Captura as as teclas pressionadas
    player.update(pressed_keys) #Atualiza a posicao do player conforme teclas usadas
    enemies.update() #Atualiza posicao dos inimigos
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect) #Atualiza a exibicao de todos os Sprites

    if pygame.sprite.spritecollideany(player, enemies): #Verifica se ocorreu a colisao do player com um dos inimigos
        player.kill() #Se ocorrer a colisao, encerra o player

    pygame.display.flip() #Atualiza a projecao do jogo