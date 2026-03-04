import pygame

# Быстрые Данные

WIDTH = 720
HEIGHT = 720
FPS = 30
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

# Спрайты

class Player1(pygame.sprite.Sprite): # Игрок
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.direction = 'up'

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_RIGHT]: # Направления Движения
            self.speedx = 5
            self.direction = 'right'
        elif keystate[pygame.K_LEFT]:
            self.speedx = -5
            self.direction = "left"
        elif keystate[pygame.K_UP]:
            self.speedy = -5
            self.direction = "up"
        elif keystate[pygame.K_DOWN]:
            self.speedy = 5
            self.direction = "down"
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite): # Пуля
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        if player1.direction == 'up': # Направления Стрельбы
            self.speedy = -10
            self.speedx = 0
        elif player1.direction == 'down':
            self.speedy = 10
            self.speedx = 0
        elif player1.direction == 'right':
            self.speedx = 10
            self.speedy = 0
        elif player1.direction == 'left':
            self.speedx = -10
            self.speedy = 0
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.bottom < 0 or self.rect.bottomleft < (0, 0) or self.rect.bottomleft > (720, 720) or self.rect.bottom > 720:
            self.kill()

        if self.rect.colliderect(wall.rect):
            wall.kill()
            self.kill()

class Wall(pygame.sprite.Sprite): # Стена
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (5, 5)

# Данные Игры

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
walls = pygame.sprite.Group()

player1 = Player1()
wall = Wall()
all_sprites.add(player1, wall)

# Игра

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player1.shoot()

    print(player1.direction, bullets)
    all_sprites.update()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()