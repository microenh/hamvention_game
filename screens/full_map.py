from typing import Callable, Optional, Tuple
import pygame

from .level_base import LevelBase

TILE_SIZE = 32
MOVEMENT = TILE_SIZE // 8

bg_color: pygame.Color = pygame.Color('gray80')
transparent: pygame.Color = pygame.Color(255,255,255)
wall_color: pygame.Color = pygame.Color('brown')
interior_color: pygame.Color = pygame.Color('gray90')
title_color: pygame.Color = pygame.Color('red')

class Building:
    pygame.font.init()
    ldoor_surf: pygame.Surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    ldoor_surf.fill(interior_color)
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
        self.surf.fill(interior_color)
        pygame.draw.rect(self.surf,
                         wall_color,
                         self.rect, width = 2)
        title_surf = self.font.render(title, True, title_color)
        title_rect = title_surf.get_rect(center = self.rect.center)
        self.surf.blit(title_surf, title_rect)
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

    def hit(self, target: pygame.Rect) -> int:
        """
        return: 0 if not hit,
                1 if hit wall
                2 if hit door
        """
        if self.rect.colliderect(target):
            for i in self.door_rects:
                if i.colliderect(target):
                    return 2
            else:
                return 1
        else:
            return 0
        
    def render(self, surface: pygame.Surface,
               offset_x: int, offset_y: int):
        r: pygame.Rect = self.rect.move(offset_x, offset_y)
        surface.blit(self.surf, r)
        


class FullMap(LevelBase):


    def __init__(self, rect: pygame.Rect,
                 set_next: Callable[[Optional[str]], None]) -> None:
        super().__init__(rect, set_next)

        self.buildings: Tuple[Building, ...] = (
            Building(1, 1, 4, 5, (), (1,), (), (2,), 'Maxim', 'maxim'),
            Building(7, 1, 6, 5, (1,), (1,), (), (3,), 'Tesla', 'tesla'),
            Building(15, 1, 4, 5, (1,), (), (), (2,), 'Marconi', 'marconi'),
        )

        self.ham_surf: pygame.Surface = (
            pygame.image.load('graphics/w8bi.png').convert_alpha())
        self.ham_rect: pygame.Rect = (
            self.ham_surf.get_rect(midbottom=rect.midbottom))
        self.mvmt_x = self.mvmt_y = 0
        self.offset_x = self.offset_y = 0

    def event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                        self.set_next('end')
                    case pygame.K_UP:
                        self.mvmt_y = -1
                    case pygame.K_DOWN:
                        self.mvmt_y = 1
                    case pygame.K_LEFT:
                        self.mvmt_x = -1
                    case pygame.K_RIGHT:
                        self.mvmt_x = 1
            case pygame.KEYUP:
                match event.key:
                    case pygame.K_UP | pygame.K_DOWN:
                        self.mvmt_y = 0
                    case pygame.K_LEFT | pygame.K_RIGHT:
                        self.mvmt_x = 0

    def update(self):
        if self.mvmt_x or self.mvmt_y:
            r = self.ham_rect.move(self.mvmt_x * MOVEMENT,
                                   self.mvmt_y * MOVEMENT)
            update = True
            for i in self.buildings:
                match i.hit(r):
                    case 0:
                        continue
                    case 1:
                        update = False
                    case 2:
                        self.set_next(i.dest)
                        break
            if update:        
                self.ham_rect = r
        
                
    def render(self, surface: pygame.Surface) -> None:
        surface.fill(bg_color)
        for i in self.buildings:
            i.render(surface, self.offset_x, self.offset_y)
        surface.blit(self.ham_surf, self.ham_rect)
        
    
    
