from typing import Callable, Optional, Tuple
import pygame

from .building import Building
from .area import Area
from .level_base import LevelBase
from .setup import bg_color, MARGIN, MOVEMENT, saved_position, TILE_SIZE

class FullMap(LevelBase):
    def __init__(self, rect: pygame.Rect,
                 set_next: Callable[[Optional[str]], None]) -> None:
        super().__init__(rect, set_next)

        self.buildings: Tuple[Building, ...] = (
            Building(16,  4, 5, 5, (), (1,), (), (2,), 'Maxim', 'maxim'),
            Building(23,  4, 5, 5, (1,), (1,), (), (3,), 'Tesla', 'tesla'),
            Building(30,  4, 5, 5, (1,), (), (), (2,), 'Marconi', 'marconi'),
            Building(38,  5, 4, 3, (1,), (), (), (), 'Forum 4', 'forum4'),
            Building( 4, 15, 7, 3, (1,), (1,), (), (), 'Tent', 'tent'),
            Building(16, 13, 3, 4, (2,), (), (), (), 'Forum 1', 'forum1'),
            Building(16, 17, 3, 4, (1,), (), (), (), 'Forum 2', 'forum2'),
            Building(22, 15, 3, 4, (1,), (), (), (), 'Forum 3', 'forum3'),
            Building(27, 15, 3, 4, (), (1,), (1,), (1,), 'Hertz', 'hertz'),
            Building(32, 13, 3, 6, (2,), (2,), (1,), (1,), 'Volta', 'volta'),
        )

        self.areas: Tuple[Area, ...] = (
            Area(16,  0, 26,  2, 'Campers', 'campers'),
            Area( 0,  5,  3,  2, 'Tickets', 'tickets'),
            Area( 0, 23,  3,  2, 'Testing', 'testing'),
            Area( 4, 11,  4,  2, 'Forum 5', 'forum5'),
            Area( 8, 11,  4,  2, 'Emcomm', 'emcomm'),
            Area(16, 24, 26,  2, 'Flea Market', 'flea_market'),
            Area(23, 10,  5,  2, 'Food', 'food'),
            Area(44,  4,  6, 22, 'Flea Market', 'flea_market'),
        )

        self.ham_surf: pygame.Surface = (
            pygame.image.load('graphics/w8bi.png').convert_alpha())

        self.ham_rect: pygame.Rect = self.ham_surf.get_rect()
        self.ham_rect.x = saved_position[0]
        self.ham_rect.y = saved_position[1]
        
        self.vel_x = self.vel_y = 0

        self.vel_offset_x = self.vel_offset_y = 0
        self.offset_x = self.offset_y = 0

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
                self.ham_rect = r

            
    def render(self, surface: pygame.Surface) -> None:
        surface.fill(bg_color)
        sr = surface.get_rect()
        r = self.ham_rect.move(self.offset_x, self.offset_y)
        if r.left < sr.left + MARGIN:
            self.offset_x += sr.left + MARGIN - r.left
        elif r.right > sr.right - MARGIN:
            self.offset_x += sr.right - MARGIN - r.right
        if r.top < sr.top + 20:
            self.offset_y += sr.top + MARGIN - r.top
        elif r.bottom > sr.bottom - MARGIN:
            self.offset_y += sr.bottom - MARGIN - r.bottom
        r = self.ham_rect.move(self.offset_x, self.offset_y)
            
        for i in self.buildings:
            i.render(surface, self.offset_x, self.offset_y)
        for j in self.areas:
            j.render(surface, self.offset_x, self.offset_y)
            
        surface.blit(self.ham_surf, r)
        
            
        
    
    
