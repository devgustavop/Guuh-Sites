import pygame
import random

# Inicializa o pygame
pygame.init()

# Dimensões da tela
screen_width = 1200
screen_height = 600

# Configurações da tela
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo da Nave Espacial")

# Cores
black = (0, 0, 0)
white = (255, 255, 255)

# Carregar imagens
spaceship_image = pygame.image.load("spaceship.png")
asteroid_image = pygame.image.load("asteroid.png")
bullet_image = pygame.image.load("bullet.png")

# Dimensões da nave
spaceship_width = 64
spaceship_height = 64

# Posições iniciais da nave
spaceship_x = screen_width // 2 - spaceship_width // 2
spaceship_y = screen_height - spaceship_height - 10

# Velocidade da nave
spaceship_speed = 5

# Lista para armazenar as balas
bullets = []

# Lista para armazenar os asteroides
asteroids = []

# Função para desenhar a nave
def draw_spaceship(x, y):
    screen.blit(spaceship_image, (x, y))

# Função para desenhar uma bala
def draw_bullet(x, y):
    screen.blit(bullet_image, (x, y))

# Função para desenhar um asteroide
def draw_asteroid(x, y):
    screen.blit(asteroid_image, (x, y))

# Função principal do jogo
def game_loop():
    global spaceship_x, spaceship_y
    
    # Variável para controlar o loop principal
    running = True

    # Relógio para controlar a taxa de frames
    clock = pygame.time.Clock()

    # Pontuação
    score = 0

    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_x = spaceship_x + spaceship_width // 2 - 4
                    bullet_y = spaceship_y
                    bullets.append([bullet_x, bullet_y])

        # Movimentação da nave
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship_x > 0:
            spaceship_x -= spaceship_speed
        if keys[pygame.K_RIGHT] and spaceship_x < screen_width - spaceship_width:
            spaceship_x += spaceship_speed
        if keys[pygame.K_UP] and spaceship_y > 0:
            spaceship_y -= spaceship_speed
        if keys[pygame.K_DOWN] and spaceship_y < screen_height - spaceship_height:
            spaceship_y += spaceship_speed

        # Movimentação das balas
        for bullet in bullets:
            bullet[1] -= 10
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Adicionar novos asteroides
        if random.randint(1, 50) == 1:
            asteroid_x = random.randint(0, screen_width - 64)
            asteroid_y = -64
            asteroids.append([asteroid_x, asteroid_y])

        # Movimentação dos asteroides
        for asteroid in asteroids:
            asteroid[1] += 5
            if asteroid[1] > screen_height:
                asteroids.remove(asteroid)
                score -= 1

        # Colisão entre balas e asteroides
        for bullet in bullets:
            for asteroid in asteroids:
                if (bullet[0] < asteroid[0] + 64 and bullet[0] + 8 > asteroid[0] and
                    bullet[1] < asteroid[1] + 64 and bullet[1] + 8 > asteroid[1]):
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    score += 1
                    break

        # Colisão entre a nave e os asteroides
        for asteroid in asteroids:
            if (spaceship_x < asteroid[0] + 64 and spaceship_x + spaceship_width > asteroid[0] and
                spaceship_y < asteroid[1] + 64 and spaceship_y + spaceship_height > asteroid[1]):
                running = False

        # Desenhar a tela
        screen.fill(black)
        draw_spaceship(spaceship_x, spaceship_y)
        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1])
        for asteroid in asteroids:
            draw_asteroid(asteroid[0], asteroid[1])

        # Mostrar pontuação
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Pontuação: {score}", True, white)
        screen.blit(score_text, (10, 10))

        # Atualizar a tela
        pygame.display.flip()

        # Controlar a taxa de frames
        clock.tick(60)

    pygame.quit()

# Chamar a função principal do jogo
game_loop()
