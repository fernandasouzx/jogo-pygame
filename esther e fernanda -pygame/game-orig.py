 # Biblioteca PyGame
import pygame
# Biblioteca para geracao de numeros pseudoaleatorios
import random
# Modulo da biblioteca PyGame que permite o acesso as teclas utilizadas
from pygame.locals import *


GAME_STATE = "START" # START ou RUNNING ou GAME_OVER

score = 0
difficult_time =  1
kill = False

## Classe que representar o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        nave = pygame.image.load('nave.png') #importa imagem 
        super(Player, self).__init__()
        self.surf = nave
        self.rect = self.surf.get_rect()




    # Determina acao de movimento conforme teclas pressionadas
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)

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
        asteroide = pygame.image.load('asteroid.png') #importa imagem 
        super(Enemy, self).__init__()
        self.surf = asteroide
        self.rect = self.surf.get_rect( #Coloca na extrema direita (entre 820 e 900) e sorteia sua posicao em relacao a coordenada y (entre 0 e 600)
            center=(random.randint(720, 800), random.randint(0, 600))
        )
        self.speed = random.uniform(1, 8) * difficult_time#Sorteia sua velocidade, entre 1 e 15

    # Funcao que atualiza a posiçao do inimigo em funcao da sua velocidade e termina com ele quando ele atinge o limite esquerdo da tela (x < 0)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


def initial_screen(pygame,screen): 
    pygame.display.set_caption("Inicio de jogo")
    fundo = pygame.image.load('startgame.png')
    background = fundo
    
    running = True
    while running:
        
        for event in pygame.event.get():
            
            if event.type == KEYDOWN:
                if event.key == K_SPACE: #Verifica se a tecla espaço foi pressionada para começar o jogo
                    running = False
                    return True
            elif event.type == QUIT: #Verifica se a janela foi fechada
                running = False
                return False
        screen.blit(background, (0, 0)) #Atualiza a exibicao do plano de fundo do jogo (neste caso nao surte efeito)    
        pygame.display.flip() #Atualiza a projecao do jogo
def start_screen(pygame,screen):
    global score, difficult_time, kill
    pygame.display.set_caption("Jogue")

    # Cria um evento para adicao de inimigos
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 800) #Define um intervalo para a criacao de cada inimigo (milisegundos)
    ADDTIME = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDTIME, 1000)

    UPDIFFICULT = pygame.USEREVENT + 3 #aumenta dificuldade do jogo ao passar 10 segundos
    pygame.time.set_timer(UPDIFFICULT, 10000)

    # Cria o jogador (Personagem Asteroide)
    player = Player()

    # Define o plano de fundo, com imagem 
    background = pygame.Surface(screen.get_size())
    fundo = pygame.image.load('fundo.png')
    background = fundo

    enemies = pygame.sprite.Group() #Cria o grupo de inimigos
    all_sprites = pygame.sprite.Group() #Cria o grupo de todos os Sprites
    all_sprites.add(player) #Adicionar  o player no grupo de todos os Sprites

    # define a pontuação
    clock = pygame.time.Clock()


    font = pygame.font.Font('pricedow.ttf',60)
    auxFont = pygame.font.Font('pricedow.ttf',30)
    text = font.render("Score: " + str(score), True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (400, 60)

    textLevel = auxFont.render("level: " + str(difficult_time), True, (255,255,255, 0.5))
    textLevelRect = textLevel.get_rect()
    textLevelRect.center = (730, 30)

    running = True #Flag para controle do jogo

    while running:
        #Laco para verificacao do evento que ocorreu
        clock.tick(60)

        for event in pygame.event.get():
            #score
            if (event.type == ADDTIME) and kill == False:
                score += 1
                text = font.render("Score:"+ str(score), True, (255, 255, 255))
            if (event.type == UPDIFFICULT): # a cada 10s
                difficult_time = difficult_time + 1
                textLevel = auxFont.render("Level: " + str(difficult_time), True, (255,255,255, 0.5))
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
        screen.blit(text, textRect) # mostra o score na tela
        screen.blit(textLevel, textLevelRect) # mostra o level na tela
        pressed_keys = pygame.key.get_pressed() #Captura as as teclas pressionadas
        player.update(pressed_keys) #Atualiza a posicao do player conforme teclas usadas
        enemies.update() #Atualiza posicao dos inimigos
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect) #Atualiza a exibicao de todos os Sprites

        if pygame.sprite.spritecollideany(player, enemies): #Verifica se ocorreu a colisao do player com um dos inimigos
            player.kill() #Se ocorrer a colisao, encerra o player
            kill = True
            running = False

        pygame.display.flip() #Atualiza a projecao do jogo

def gameover_screen(pygame,screen):
    pygame.display.set_caption("Game Over! :(")
    fundo = pygame.image.load('gameover.png')
    background = fundo
    
    font = pygame.font.Font('pricedow.ttf',60)
    pontuacao = pygame.font.Font('pricedow.ttf',30)
    text = font.render("Score: " + str(score), True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (400, 400)

    txe = font.render("Level " + str(difficult_time), True, (255,255,255))
    txetRect = txe.get_rect()
    txetRect.center = (400, 450)

    
    running = True
    while running:
        
        for event in pygame.event.get():
            
            if event.type == KEYDOWN:
                if event.key == K_SPACE: #verififica se a tecla de espaço foi pressionada
                    running = False
                    return True
            elif event.type == QUIT: #Verifica se a janela foi fechada
                running = False
                return False
       
        
        screen.blit(background, (0, 0)) #Atualiza a exibicao do plano de fundo do jogo (neste caso nao surte efeito)    
        screen.blit(text, textRect) # mostra o score na tela
        screen.blit(txe, txetRect) #mostra o nivel na tela

        pygame.display.flip() #Atualiza a projecao do jogo
   

if __name__ == "__main__":
   
   # Inicializa pygame
    pygame.init()


    # Adiciona musica
    pygame.mixer.music.load('audio.mp3')
    pygame.mixer.music.play(-1)

    # Cria a tela com resolução 800x600px
    screen = pygame.display.set_mode((800, 600))

   
    valor = initial_screen(pygame, screen)
    if valor is True:
        running = True
        while running:
            score = 0
            difficult_time =  1
            kill = False
            
            start_screen(pygame, screen)
            running = gameover_screen(pygame, screen)