from typing import Tuple
import pygame

from .setup import (TILE_SIZE, transparent, wall_color,
                    building_color, building_title_color)

class Building:
    pygame.font.init()
    ldoor_surf: pygame.Surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    ldoor_surf.fill(building_color)
    pygame.draw.line(ldoor_surf,
                     transparent,
                     (0, 0),
                     (0, TILE_SIZE-2),
                     width=2)
    pygame.draw.line(ldoor_surf,
                     wall_color,
                     (0, TILE_SIZE-1),
                     (TILE_SIZE // 3, TILE_SIZE // 8),
                     width=2)
    rdoor_surf = pygame.transform.flip(ldoor_surf, True, True)
    tdoor_surf = pygame.transform.rotate(ldoor_surf, -90)
    bdoor_surf = pygame.transform.flip(tdoor_surf, True, True)
    font: pygame.font.Font = pygame.font.Font(None, 32)
    
    def __init__(self, x: int, y: int, w: int, h: int,
                 l_doors: Tuple[int, ...],
                 r_doors: Tuple[int, ...],
                 t_doors: Tuple[int, ...],
                 b_doors: Tuple[int, ...],
                 title: str,
                 dest: str) -> None:

        screen_x: int = x * TILE_SIZE
        screen_y: int = y * TILE_SIZE

        self.dest = dest

        self.surf: pygame.Surface = pygame.Surface((w * TILE_SIZE, h * TILE_SIZE))
        self.rect: pygame.Rect = self.surf.get_rect()
        self.surf.set_colorkey(transparent)
        self.surf.fill(building_color)
        pygame.draw.rect(self.surf,
                         wall_color,
                         self.rect, width = 2)
        title_surf = self.font.render(title, True, building_title_color)
        title_rect = title_surf.get_rect(center = self.rect.center)
        self.rect.move_ip(screen_x, screen_y)
        self.door_rects: list[pygame.Rect] = []
        for i in l_doors:
            d: pygame.Rect = pygame.Rect(
                0, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            self.surf.blit(self.ldoor_surf, d)
            self.door_rects.append(d.move(screen_x, screen_y))
        for i in r_doors:
            d = pygame.Rect(
                (w - 1) * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            self.surf.blit(self.rdoor_surf, d)
            self.door_rects.append(d.move(screen_x, screen_y))
        for i in t_doors:
            d = pygame.Rect(
                i * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
            self.surf.blit(self.tdoor_surf, d)
            self.door_rects.append(d.move(screen_x, screen_y))
        for i in b_doors:
            d = pygame.Rect(
                i * TILE_SIZE, (h - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            self.surf.blit(self.bdoor_surf, d)
            self.door_rects.append(d.move(screen_x, screen_y))
        self.surf.blit(title_surf, title_rect)

    def hit(self, target: pygame.Rect) -> int:
        """
        return: 0 if not hit,
                1 if hit wall
                2 if hit door
        """
        return ((1 if target.collidelist(self.door_rects) == -1 else 2)
            if target.colliderect(self.rect) else 0)
        
    def render(self, surface: pygame.Surface,
               offset_x: int, offset_y: int):
        r: pygame.Rect = self.rect.move(offset_x, offset_y)
        if r.colliderect(surface.get_rect()):
            surface.blit(self.surf, r)
