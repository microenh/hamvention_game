from typing import Callable, Optional, Tuple
import pygame

from .level_base import LevelBase

TILE_SIZE = 32

bg_color: pygame.Color = pygame.Color('gray80')
transparent: pygame.Color = pygame.Color(255,255,255)
wall_color: pygame.Color = pygame.Color('brown')
interior_color: pygame.Color = pygame.Color('gray90')

class FullMap(LevelBase):
    def __init__(self, rect: pygame.Rect,
                 set_next: Callable[[Optional[str]], None]) -> None:
        super().__init__(rect, set_next)

        self.mvmt_x = 0
        self.mvmt_y = 0

        self.building_surf: pygame.Surface = self.building(150, 300, (), (), (), ()) 


        self.ham_surf: pygame.Surface = pygame.image.load('graphics/w8bi.png').convert_alpha()
        self.ham_rect: pygame.Rect = self.ham_surf.get_rect(midbottom=rect.midbottom)
        
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

    def building(self, w: int, h: int,
                 l_doors: Tuple[int, ...],
                 r_doors: Tuple[int, ...],
                 t_doors: Tuple[int, ...],
                 b_doors: Tuple[int, ...]) -> pygame.Surface:
        r: pygame.Surface = pygame.Surface((w, h))
        r.set_colorkey(transparent)
        r.fill(interior_color)
        pygame.draw.rect(r, wall_color,
                         r.get_rect(),
                         width = 2)

        ldoor_surf: pygame.Surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        ldoor_surf.fill(interior_color)
        pygame.draw.line(ldoor_surf, transparent,
                         (0,0), (0,TILE_SIZE-2), width=2)
        pygame.draw.line(ldoor_surf, wall_color,
                         (0,TILE_SIZE-1), (TILE_SIZE // 3, TILE_SIZE // 8), width=2)

        rdoor_surf = pygame.transform.flip(ldoor_surf, True, True)
        tdoor_surf = pygame.transform.rotate(ldoor_surf, -90)
        bdoor_surf = pygame.transform.flip(tdoor_surf, True, True)

        r.blit(ldoor_surf, (0, 20))        
        # r.blit(ldoor_surf, (0, 130))
        r.blit(rdoor_surf, ((w - 1) * TILE_SIZE, 20))
        # r.blit(rdoor_surf, ((w - 1) * TILE_SIZE, 130))
        r.blit(tdoor_surf, (80, 0))
        r.blit(bdoor_surf, (80, (h - 1) * TILE_SIZE))
        

        return r
        

    def update(self):
        self.ham_rect.move_ip(self.mvmt_x, self.mvmt_y)
        
                
    def render(self, surface: pygame.Surface) -> None:
        surface.fill(bg_color)
        surface.blit(self.building_surf, (10,10))
        surface.blit(self.ham_surf, self.ham_rect)
        
    
    
