from typing import Tuple
import pygame

from .setup import (TILE_SIZE, transparent,
                    area_color, area_title_color)

class Area:
    pygame.font.init()
    font: pygame.font.Font = pygame.font.Font(None, 32)
    
    def __init__(self,
                 x: int, y: int, w: int, h: int,
                 title: str, dest: str) -> None:

        screen_x: int = x * TILE_SIZE
        screen_y: int = y * TILE_SIZE

        self.dest = dest

        self.surf: pygame.Surface = pygame.Surface((w * TILE_SIZE, h * TILE_SIZE))
        self.rect: pygame.Rect = self.surf.get_rect()
        self.surf.set_colorkey(transparent)
        self.surf.fill(transparent)
        pygame.draw.rect(self.surf,
                         area_color,
                         self.rect, border_radius = 20)
        
        title_surf = self.font.render(title, True, area_title_color)
        title_rect = title_surf.get_rect(center = self.rect.center)
        self.surf.blit(title_surf, title_rect)
        self.rect.move_ip(screen_x, screen_y)

    def hit(self, target: pygame.Rect) -> bool:
        return target.colliderect(self.rect)
        
    def render(self, surface: pygame.Surface,
               offset_x: int, offset_y: int):
        r: pygame.Rect = self.rect.move(offset_x, offset_y)
        if r.colliderect(surface.get_rect()):
            surface.blit(self.surf, r)
