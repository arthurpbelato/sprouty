from common.imports import *
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)

        self.import_assets()
        self.status = 'down'
        self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['main']

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        self.timers = {
            'tool_use': Timer(350, self.use_tool) ,
            'tool_switch' : Timer(200),
            'seed_use': Timer(350, self.use_seed) ,
            'seed_switch' : Timer(200)
        }

        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy().inflate((-126, -70))

    def use_tool(self):
        pass

    def use_seed(self):
        print(self.selected_seed)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool_use'].active:
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else: 
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else: 
                self.direction.x = 0

            if keys[pygame.K_SPACE]:
                self.timers['tool_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            if keys[pygame.K_q] and not self.timers['tool_switch'].active:
                self.timers['tool_switch'].activate()
                self.tool_index += 1
                if self.tool_index >= len(self.tools):
                    self.tool_index = 0
                self.selected_tool = self.tools[self.tool_index]

            if keys[pygame.K_LCTRL]:
                self.timers['seed_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            if keys[pygame.K_e] and not self.timers['seed_switch'].active:
                self.timers['seed_switch'].activate()
                self.seed_index += 1
                if self.seed_index >= len(self.seeds):
                    self.seed_index = 0
                self.selected_seed = self.seeds[self.seed_index]

    def collision(self, direction): 
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if(direction == 'horizontal'):
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if(direction == 'vertical'):
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.horizontal_move(dt)
        self.vertical_move(dt)

    def horizontal_move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx =  round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

    def vertical_move(self, dt):
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery =  round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animate(dt)

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                        'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                        'up_axe': [], 'down_axe': [], 'left_axe': [], 'right_axe': [],
                        'up_water': [], 'down_water': [], 'left_water': [], 'right_water': [],
                        'up_hoe': [], 'down_hoe': [], 'left_hoe': [], 'right_hoe': [],}

        for animation in self.animations.keys():
            full_path = Graphics.CHARACTER + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        if self.timers['tool_use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
