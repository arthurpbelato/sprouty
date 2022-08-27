from sprites import Generic
from common.imports import *
from support import import_folder
from random import choice, randint

class Drop(Generic):
    def __init__(self, pos, surf, moving, groups, z):
        
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)

    def update(self, dt):
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = import_folder(Graphics.RAIN_DROPS)
        self.rain_floor = import_folder(Graphics.RAIN_FLOOR)
        self.floor_w, self.floor_h = pygame.image.load(f'{Graphics.WORLD}ground.png').get_size()

    def create_floor(self):
        Drop(
            pos = (randint(0, self.floor_w), randint(0, self.floor_h)),
            surf = choice(self.rain_floor),
            moving = False,
            groups = self.all_sprites,
            z = LAYERS['rain_floor'])

    def create_drops(self):
        Drop(
            pos = (randint(0, self.floor_w), randint(0, self.floor_h)),
            surf = choice(self.rain_drops),
            moving = True,
            groups = self.all_sprites,
            z = LAYERS['rain_drops'])

    def update(self):
        self.create_drops()
        self.create_floor()