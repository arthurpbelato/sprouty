from pygame.math import Vector2

TITLE = 'Sprouty'
VERSION = 'v0.0'
CAPTION = TITLE + ' ' + VERSION

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50,40),
    'right': Vector2(50,40),
    'up': Vector2(0,-10),
    'down': Vector2(0,50)
}

OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'seed': (70, SCREEN_HEIGHT - 5)
}

class Graphics:
    ROOT = 'graphics/'
    CHARACTER = ROOT + 'character/' 
    OVERLAY = ROOT + 'overlay/'
    WORLD = ROOT + 'world/'
    WATER = ROOT + 'water/'
    FRUIT = ROOT + 'fruit/'
    STUMPS = ROOT + 'stumps/'
    SOIL = ROOT + 'soil/'
    SOIL_WATER = ROOT + 'soil_water/'

LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil_water': 3,
    'rain_floor': 4,
    'house_bottom': 5,
    'ground_plant': 6,
    'main': 7,
    'house_top': 8,
    'fruit': 9,
    'rain_drops': 10
}

APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

