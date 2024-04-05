from typing import Callable, Optional, Tuple
import pygame

from .building import Building
from .area import Area
from .level_base import LevelBase
from .setup import (bg_color, MARGIN, MOVEMENT, saved_position, TILE_SIZE,
                    transparent, fps_font, fps_color, fps_border_color,
                    SCREEN_SIZE, MAX_MAP)

class FullMap(LevelBase):
    def __init__(self, rect: pygame.Rect,
                 set_next: Callable[[Optional[str]], None]) -> None:
        super().__init__(rect, set_next)

        self.buildings: Tuple[Building, ...] = (
            Building(17,  6, 5, 5, (), (1,), (), (2,), 'Maxim', 'maxim'),
            Building(24,  6, 5, 5, (1,), (1,), (), (3,), 'Tesla', 'tesla'),
            Building(31,  6, 5, 5, (1,), (), (), (2,), 'Marconi', 'marconi'),
            Building(38,  7, 4, 3, (1,), (), (), (), 'Forum 4', 'forum4'),
            Building( 7, 17, 8, 4, (1,), (1,), (), (), 'Tent', 'tent'),
            Building(17, 15, 3, 4, (2,), (), (), (), 'Forum 1', 'forum1'),
            Building(17, 19, 3, 4, (1,), (), (), (), 'Forum 2', 'forum2'),
            Building(23, 17, 3, 4, (1,), (), (), (), 'Forum 3', 'forum3'),
            Building(28, 17, 3, 4, (), (1,), (1,), (1,), 'Hertz', 'hertz'),
            Building(33, 15, 3, 6, (2,), (2,), (1,), (1,), 'Volta', 'volta'),
        )

        self.areas: Tuple[Area, ...] = (
            Area(17,  2, 25,  2, 'Campers', 'campers'),
            Area( 2,  7,  3,  2, 'Tickets', 'tickets'),
            Area( 2, 26,  3,  2, 'Testing', 'testing'),
            Area( 7, 13,  4,  2, 'Forum 5', 'forum5'),
            Area(11, 13,  4,  2, 'Emcomm', 'emcomm'),
            Area(22, 13,  9,  2, 'Food', 'food'),
            Area(44,  6,  6, 22, 'Flea Market', 'flea_market'),
            Area(17, 26, 25,  2, 'Flea Market', 'flea_market'),
        )

        self.ham_surf: pygame.Surface = (
            pygame.image.load('graphics/w8bi.png').convert_alpha())

        self.ham_rect: pygame.Rect = self.ham_surf.get_rect()
        self.ham_rect.x = saved_position[0]
        self.ham_rect.y = saved_position[1]
        
        self.vel_x = self.vel_y = 0

        self.vel_offset_x = self.vel_offset_y = 0
        self.offset_x = self.offset_y = 0

        xy_size = fps_font.size('00000,00000')
        self.xy_border_surf: pygame.Surface = pygame.Surface((xy_size[0] + 20,
                                                              xy_size[1] + 4))
        self.xy_border_rect: pygame.Rect = self.xy_border_surf.get_rect()
        pygame.draw.rect(self.xy_border_surf,
                         fps_border_color,
                         self.xy_border_rect,
                         border_radius=8)
        self.xy_border_rect.left = 4
        self.xy_border_rect.bottom = SCREEN_SIZE[1] - 4
        
        self.xy_border_surf.set_colorkey(transparent)
        self.xy_surf: pygame.Surface = fps_font.render('', True, fps_color)
        self.xy_rect: pygame.Rect = self.xy_surf.get_rect(center = self.xy_border_rect.center)

    def event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                        self.set_next('end')
                    case pygame.K_UP:
                        self.vel_y = -1
                    case pygame.K_DOWN:
                        self.vel_y = 1
                    case pygame.K_LEFT:
                        self.vel_x = -1
                    case pygame.K_RIGHT:
                        self.vel_x = 1
                    case pygame.K_w:
                        self.vel_offset_y = -1
                    case pygame.K_s:
                        self.vel_offset_y = 1
                    case pygame.K_a:
                        self.vel_offset_x = -1
                    case pygame.K_d:
                        self.vel_offset_x = 1
            case pygame.KEYUP:
                match event.key:
                    case pygame.K_UP | pygame.K_DOWN:
                        self.vel_y = 0
                    case pygame.K_LEFT | pygame.K_RIGHT:
                        self.vel_x = 0
                    case pygame.K_w | pygame.K_s:
                        self.vel_offset_y = 0
                    case pygame.K_a | pygame.K_d:
                        self.vel_offset_x = 0

    def update(self):
        self.offset_x += self.vel_offset_x * MOVEMENT
        self.offset_y += self.vel_offset_y * MOVEMENT
        
        if self.vel_x or self.vel_y:
            r = self.ham_rect.move(self.vel_x * MOVEMENT,
                                   self.vel_y * MOVEMENT)
            update = True
            for i in self.buildings:
                match i.hit(r):
                    case 0:
                        continue
                    case 1:
                        update = False
                    case 2:
                        saved_position[0] = i.rect.x - TILE_SIZE
                        saved_position[1] = i.rect.y - TILE_SIZE
                        self.set_next(i.dest)
                        break
                    
            for i in self.areas:
                if i.hit(r):
                    saved_position[0] = i.rect.x - TILE_SIZE
                    saved_position[1] = i.rect.y - TILE_SIZE
                    self.set_next(i.dest)
                    
            if update:
                if r.right > MAX_MAP[0]:
                    r.right = MAX_MAP[0]
                elif r.left < 0:
                    r.left = 0
                if r.top < 0:
                    r.top = 0
                elif r.bottom > MAX_MAP[1]:
                    r.bottom = MAX_MAP[1]
                self.ham_rect = r
        self.xy_surf = fps_font.render(f'{self.ham_rect.x}, {self.ham_rect.y}', True, fps_color)
        self.xy_rect = self.xy_surf.get_rect(center=self.xy_border_rect.center)

            
    def render(self, surface: pygame.Surface) -> None:
        surface.fill(bg_color)
        sr = surface.get_rect()
        r = self.ham_rect.move(self.offset_x, self.offset_y)
        if r.left < sr.left + MARGIN:
            self.offset_x += sr.left + MARGIN - r.left
        elif r.right > sr.right - MARGIN:
            self.offset_x += sr.right - MARGIN - r.right
        if r.top < sr.top + MARGIN:
            self.offset_y += sr.top + MARGIN - r.top
        elif r.bottom > sr.bottom - MARGIN:
            self.offset_y += sr.bottom - MARGIN - r.bottom
        r = self.ham_rect.move(self.offset_x, self.offset_y)
            
        for i in self.buildings:
            i.render(surface, self.offset_x, self.offset_y)
        for j in self.areas:
            j.render(surface, self.offset_x, self.offset_y)


        surface.blit(self.xy_border_surf, self.xy_border_rect)
        surface.blit(self.xy_surf, self.xy_rect)            

        surface.blit(self.ham_surf, r)
        
            
        
    
    
