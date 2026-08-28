from pygame import Surface, constants, display, event, init, key, mixer, time, quit
from pygame.sprite import Group, Sprite
from WorldGen import generate_hor, generate_ver, ungenerate

# Быстрые Данные

WIDTH = 720
HEIGHT = 720
FPS = 30
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
flag_destruction = False

# Спрайты


class Player(Sprite):  # Игрок База
    def __init__(self, spawnx, spawny, color, right_key, left_key, up_key, down_key):
        Sprite.__init__(self)
        self.image = Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (spawnx, spawny)
        self.direction = 'up'

        self.right_key = right_key
        self.left_key = left_key
        self.up_key = up_key
        self.down_key = down_key

    def update(self):
        self.speedx = 0
        self.speedy = 0
        key_state = key.get_pressed()

        if key_state[self.right_key]:  # <- Направления Движения
            self.speedx = 5
            self.direction = 'right'
        elif key_state[self.left_key]:
            self.speedx = -5
            self.direction = 'left'
        elif key_state[self.up_key]:
            self.speedy = -5
            self.direction = 'up'
        elif key_state[self.down_key]:
            self.speedy = 5
            self.direction = 'down'

        for wall in walls:  # <- Коллизия c Препядствиями
            if (self.rect.top == 0 and self.direction == 'up') or (self.rect.bottom == HEIGHT and self.direction == 'down'):  # <- Коллизия с Границами
                self.speedy = 0
            elif (self.rect.left == 0 and self.direction == 'left') or (self.rect.right == WIDTH and self.direction == 'right'):
                self.speedx = 0 

            if (self.rect.top == wall.rect.bottom and wall.rect.x - 20 < self.rect.x < wall.rect.x + 10 and self.direction == 'up'):  # <- Коллизия с Стенами
                self.speedy = 0
            elif (self.rect.bottom == wall.rect.top and wall.rect.x - 20 < self.rect.x < wall.rect.x + 10 and self.direction == 'down'):
                self.speedy = 0
            elif (self.rect.left == wall.rect.right and wall.rect.y - 20 < self.rect.y < wall.rect.y + 10 and self.direction == 'left'):
                self.speedx = 0
            elif (self.rect.right == wall.rect.left and wall.rect.y - 20 < self.rect.y < wall.rect.y + 10 and self.direction == 'right'):
                self.speedx = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)

class PlayerRed(Player):  # Игрок Красный
    def __init__(self, spawnx, spawny, color, right_key, left_key, up_key, down_key):
        super().__init__(spawnx, spawny, color, right_key, left_key, up_key, down_key)

    def update(self):
        super().update()
        
class PlayerBlue(Player):  # Игрок Синий
    def __init__(self, spawnx, spawny, color, right_key, left_key, up_key, down_key):
        super().__init__(spawnx, spawny, color, right_key, left_key, up_key, down_key)

    def update(self):
        super().update()

class Bullet(Sprite):  # Пуля
    def __init__(self, x: float, y: float):
        Sprite.__init__(self)
        self.image = Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        if player1.direction == 'up':  # <- Направления Стрельбы
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
        global flag_destruction

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.bottom < 0 or self.rect.bottomleft < (0, 0) or self.rect.bottomleft > (720, 720) or self.rect.bottom > 720:  # <- Уничтожение за Краями
            self.kill()

        if self.rect.colliderect(flag.rect): # <- Уничтожение Флага
            self.kill()
            flag_destruction = True

        if self.rect.colliderect(player1.rect): # <- Столкновение с Игроком
            print('ы') 

        for wall in walls:  # <- Уничтожение Стены
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

class Flag(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 10)

# Данные Игры

init()
mixer.init()
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()

all_sprites: Group[PlayerRed | Bullet | Wall | Flag] = Group()
bullets: Group[Bullet] = Group()
walls: Group[Wall | Flag] = Group()

player1 = PlayerRed(spawnx = WIDTH / 2, spawny = HEIGHT - 70, color = RED, right_key = constants.K_RIGHT, left_key = constants.K_LEFT, up_key = constants.K_UP, down_key = constants.K_DOWN)
player2 = PlayerRed(spawnx = WIDTH / 2, spawny = HEIGHT / 2, color = BLUE, right_key = constants.K_d, left_key = constants.K_a, up_key = constants.K_w, down_key = constants.K_s)

flag = Flag()
all_sprites.add(player1, player2)
all_sprites.add(flag)

# Загрузка Уровня

generate_ver(32)
generate_hor(32)

level = []
with open('map.txt') as file:
    for line in file:
        level.append(line.strip())

for y in range(len(level)):
    for x, j in enumerate(level[y]):
        if j == '1' or j == '2':
            wall = Wall(x+1, y+1)
            walls.add(wall)
            all_sprites.add(wall)

# Игра

countdown = 240
countdown_timer = event.custom_type()

time.set_timer(countdown_timer, 1000)
running = True

cooldown_red = time.get_ticks()  # <- Перезарядка до разницы с общим временем (первый выстрел без задержки)
cooldown_blue = time.get_ticks()

while running:
    clock.tick(FPS)

    # Выключение Игры

    if countdown == 0:
        ungenerate()
        running = False

    if flag_destruction == True:
        ungenerate()
        running = False

    for e in event.get():
        if e.type == constants.QUIT: # <- Тоже Выключение Игры
            ungenerate()
            running = False
        if e.type == countdown_timer:
            countdown -= 1

        if e.type == constants.KEYDOWN:
            if e.key == constants.K_q and e.mod & constants.KMOD_CTRL:
                ungenerate()
                running = False
            if e.key == constants.K_SPACE and time.get_ticks() >= cooldown_red:
                cooldown_red = time.get_ticks() + 500  # <- Перезарядка с РАЗНИЦОЙ с общим временем
                player1.shoot()
            elif e.key == constants.K_KP_ENTER and time.get_ticks() >= cooldown_blue:
                cooldown_blue = time.get_ticks() + 500  # <- Перезарядка с РАЗНИЦОЙ с общим временем
                player2.shoot()

    display.set_caption(f'{countdown}')
    all_sprites.update()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    display.flip()

quit()
