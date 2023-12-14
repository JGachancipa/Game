import pygame
import random

pygame.init()

# Definir colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego con Pygame")

# Definir la clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

# Definir la clase del enemigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = random.randint(0, HEIGHT - 30)

    def update(self):
        # Simulamos un movimiento aleatorio de los enemigos
        self.rect.x += random.randint(-3, 3)
        self.rect.y += random.randint(-3, 3)

# Crear grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Crear jugador y enemigos
player = Player()
all_sprites.add(player)

for _ in range(5):  # Crear 5 enemigos
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Configurar el reloj
clock = pygame.time.Clock()

# Game Loop
running = True
paused = False

# Coordenadas del botón de pausa
pause_button_rect = pygame.Rect(WIDTH - 100, 10, 80, 30)

# Coordenadas de los botones del menú de pausa
resume_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 40, 100, 30)
quit_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 10, 100, 30)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            # Pausar o reanudar el juego al presionar la tecla 'P'
            paused = not paused

    if not paused:
        # Actualizar
        all_sprites.update()

        # Verificar colisiones con los enemigos
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            running = False

        # Dibujar
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        # Dibujar el botón de pausa
        pygame.draw.rect(screen, WHITE, pause_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Pausa", True, (0, 0, 0))
        screen.blit(text, (WIDTH - 90, 15))

    else:
        # Mostrar menú de pausa
        pygame.draw.rect(screen, (150, 150, 150), (WIDTH // 2 - 120, HEIGHT // 2 - 50, 240, 140))
        pygame.draw.rect(screen, WHITE, resume_button_rect)
        pygame.draw.rect(screen, WHITE, quit_button_rect)

        font = pygame.font.Font(None, 36)
        text = font.render("Juego Pausado", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 30))

        font = pygame.font.Font(None, 24)
        text = font.render("Continuar", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 35))

        text = font.render("Salir", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 15))

    pygame.display.flip()

    # Controlar la velocidad del juego
    clock.tick(30)
