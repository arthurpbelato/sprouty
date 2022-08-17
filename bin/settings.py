TITLE = 'Sprouty'
VERSION = 'v0.0'
CAPTION = TITLE + ' ' + VERSION

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'seed': (70, SCREEN_HEIGHT - 5)
}

class Graphics:
    ROOT = 'graphics/'
    CHARACTER = ROOT + 'character/' 
    OVERLAY = ROOT + 'overlay/'
    WORLD = ROOT + 'world/'

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

