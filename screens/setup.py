import pygame
from typing import List, Annotated

pygame.font.init()

SCREEN_SIZE = (1024,768)
TILE_SIZE = 32
MOVEMENT = TILE_SIZE // 4
MARGIN = TILE_SIZE * 2
MAX_TRANSITION = SCREEN_SIZE[1] // 16
MAX_MAP = (1680, 960)

transparent: pygame.Color = pygame.Color(0,0,0)
wall_color: pygame.Color = pygame.Color('brown')
building_color: pygame.Color = pygame.Color('gray90')
building_title_color: pygame.Color = pygame.Color('red')
area_color: pygame.Color = pygame.Color('darkgreen')
area_title_color: pygame.Color = pygame.Color('lightgreen')
bg_color: pygame.Color = pygame.Color('gray80')
transition_color: pygame.Color = pygame.Color('gray40')
end_color = pygame.Color('darkred')
splash_color: pygame.Color = pygame.Color('silver')
splash_title_color: pygame.Color = pygame.Color('linen')
splash_press_color: pygame.Color = pygame.Color('gold')



text_color = pygame.Color('red')
title_font = pygame.font.Font(None, 96)
text_font = pygame.font.Font(None, 32)

splash_font: pygame.font.Font = pygame.font.Font(None, 100)
splash_press_font = pygame.font.Font(None, 32)


notyet_color = pygame.Color('darkred')
notyet_text_color = pygame.Color('red')


notyet_font = pygame.font.Font(None, 96)
notyet_press_font = pygame.font.Font(None, 32)


fps_font: pygame.font.Font = pygame.font.Font(None, SCREEN_SIZE[1] // 32)
fps_color: pygame.Color = pygame.Color('gray60')
fps_border_color: pygame.Color = pygame.Color('gray30')

saved_position: Annotated[list[int], 2] = [0, 0]
