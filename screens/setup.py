import pygame
from typing import List, Annotated

TILE_SIZE = 32
MOVEMENT = TILE_SIZE // 4
MARGIN = TILE_SIZE * 2

transparent: pygame.Color = pygame.Color(255,255,255)
wall_color: pygame.Color = pygame.Color('brown')
building_color: pygame.Color = pygame.Color('gray90')
building_title_color: pygame.Color = pygame.Color('red')
area_color: pygame.Color = pygame.Color('darkgreen')
area_title_color: pygame.Color = pygame.Color('lightgreen')
bg_color: pygame.Color = pygame.Color('gray80')


saved_position: Annotated[list[int], 2] = [0, 0]
