from pygame import Surface, constants, display, event, init, key, mixer, time, quit
from pygame.sprite import Group, Sprite

# Быстрые Данные

WIDTH = 720
HEIGHT = 720
FPS = 30
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Спрайты


class Player1(Sprite):  # Игрок
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.direction = 'up'

    def update(self):
        self.speedx = 0
        self.speedy = 0
        key_state = key.get_pressed()

        if key_state[constants.K_RIGHT]:  # Направления Движения
            self.speedx = 5
            self.direction = 'right'
        elif key_state[constants.K_LEFT]:
            self.speedx = -5
            self.direction = 'left'
        elif key_state[constants.K_UP]:
            self.speedy = -5
            self.direction = 'up'
        elif key_state[constants.K_DOWN]:
            self.speedy = 5
            self.direction = 'down'

        for wall in walls:  # Коллизия c Препядствиями
            if (self.rect.top == 0 and self.direction == 'up') or (self.rect.bottom == HEIGHT and self.direction == 'down'):  # Коллизия с Границами
                self.speedy = 0
            if (self.rect.left == 0 and self.direction == 'left') or (self.rect.right == WIDTH and self.direction == 'right'):
                self.speedx = 0

            if (self.rect.top == wall.rect.bottom and wall.rect.x - 20 < self.rect.x < wall.rect.x + 10 and self.direction == 'up') or (self.rect.bottom == wall.rect.top and wall.rect.x - 20 < self.rect.x < wall.rect.x + 10 and self.direction == 'down'):  # Коллизия с Стенами
                self.speedy = 0
            if (self.rect.left == wall.rect.right and wall.rect.y - 20 < self.rect.y < wall.rect.y + 10 and self.direction == 'left') or (self.rect.right == wall.rect.left and wall.rect.y - 20 < self.rect.y < wall.rect.y + 10 and self.direction == 'right'):
                self.speedx = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(Sprite):  # Пуля
    def __init__(self, x: float, y: float):
        Sprite.__init__(self)
        self.image = Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        if player1.direction == 'up':  # Направления Стрельбы
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

        if self.rect.bottom < 0 or self.rect.bottomleft < (0, 0) or self.rect.bottomleft > (720, 720) or self.rect.bottom > 720:  # Уничтожение за Краями
            self.kill()

        for wall in walls:  # Уничтожение Стены
            if self.rect.colliderect(wall.rect):
                self.kill()
                wall.kill()
                break

class Wall(Sprite):  # Стена
    def __init__(self, x: float, y: float):
        Sprite.__init__(self)
        self.image = Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (10*x-5, 10*y-5)


# Данные Игры

init()
mixer.init()
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()

all_sprites: Group[Player1 | Bullet | Wall] = Group()
bullets: Group[Bullet] = Group()
walls: Group[Wall] = Group()

player1 = Player1()
all_sprites.add(player1)

# Загрузка Уровня

level = []
with open('map.txt') as file:
    for line in file:
        level.append(line.strip())

for y in range(len(level)):
    for x, j in enumerate(level[y]):
        if j == '1':
            wall = Wall(x+1, y+1)
            walls.add(wall)
            all_sprites.add(wall)

# Игра

running = True
while running:
    clock.tick(FPS)
    # print(f'{player1.rect.y, wall.rect.y}')

    for e in event.get():
        if e.type == constants.QUIT:
            running = False
        elif e.type == constants.KEYDOWN:
            if e.key == constants.K_q and e.mod & constants.KMOD_CTRL:
                running = False
            if e.key == constants.K_SPACE:
                player1.shoot()

    # print(time.get_ticks())
    all_sprites.update()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    display.flip()

quit()
