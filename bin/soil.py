from common.imports import *
from support import *
from pytmx.util_pygame import load_pygame
from random import choice
class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']

class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil_water']

class SoilLayer:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.water_surfs = import_folder(Graphics.SOIL_WATER)
        self.soil_surfs = import_folder_dict(Graphics.SOIL)

        self.create_soil_grid()
        self.create_hit_rects()

    def create_soil_grid(self):
        ground = pygame.image.load('graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        self.grid = [ [[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, _ in load_pygame('data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')

    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()
                if self.raining:
                    self.water_all()

    def water(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append('W')

                pos = soil_sprite.rect.topleft
                surf = choice(self.water_surfs)
                WaterTile(pos, surf, [self.all_sprites, self.water_sprites])

    def water_all(self):
            for index_row, row in enumerate(self.grid):
                for index_col, cell in enumerate(row):
                    if 'X' in cell and 'W' not in cell:
                        cell.append('W')
                        x = index_col * TILE_SIZE
                        y = index_row * TILE_SIZE
                        WaterTile((x,y), choice(self.water_surfs), [self.all_sprites, self.water_sprites])

    def remove_water(self):
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:

                    t = 'X' in self.grid[index_row - 1][index_col]
                    b = 'X' in self.grid[index_row + 1][index_col]
                    r = 'X' in row[index_col + 1]
                    l = 'X' in row[index_col - 1]

                    tyle_type = 'o'

                    if all((t,b,r,l)): 
                        tyle_type = 'x'

                    #vertical
                    if t and not any((l,r,b)): tyle_type = 'b'
                    if b and not any((t,l,r)): tyle_type = 't'  
                    if all((t,b)) and not any((l,r)): tyle_type = 'tb'

                    #horizontal
                    if all((l,r)) and not any((t,b)): tyle_type = 'lr'
                    if l and not any((t,r,b)): tyle_type = 'r'
                    if r and not any((t,l,b)): tyle_type = 'l'  

                    #diagonal
                    if all((r,b)) and not any((t,l)): tyle_type = 'tl'
                    if all((t,l)) and not any((r,b)): tyle_type = 'br'
                    if all((t,r)) and not any((l,b)): tyle_type = 'bl'
                    if all((b,l)) and not any((r,t)): tyle_type = 'tr'

                    #three sides covered
                    if all((t,l,b)) and not r: tyle_type = 'rm'
                    if all((r,l,b)) and not t: tyle_type = 'lrt'
                    if all((r,l,t)) and not b: tyle_type = 'lrb'
                    if all((r,t,b)) and not l: tyle_type = 'lm'

                    SoilTile(
                        pos = (index_col * TILE_SIZE, index_row * TILE_SIZE),
                        surf = self.soil_surfs[tyle_type],
                        groups=[self.all_sprites, self.soil_sprites])

