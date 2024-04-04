from typing import Callable, Optional
import pygame

from .level_base import LevelBase

bg_color: pygame.Color = pygame.Color('silver')
title_color: pygame.Color = pygame.Color('linen')
press_color: pygame.Color = pygame.Color('gold')

class Start(LevelBase):
    def __init__(self, rect: pygame.Rect,
                 set_next: Callable[[Optional[str]], None]) -> None:
        super().__init__(rect, set_next)
        self.logo: pygame.Surface = pygame.image.load('graphics/logo.png').convert_alpha()
        self.logo_rect: pygame.Rect = self.logo.get_rect()
        self.logo_vel_x: int = 4
        self.logo_vel_y: int = 4
        self.logo_rot: int = -6
        self.rotation: int = 120
        self.animate: bool = True
        self.start_delay: int = 20

        font: pygame.font.Font = pygame.font.Font(None, 100)
        self.hv_surf: pygame.Surface = font.render('Hamvention®', True, title_color)
        self.hv_rect: pygame.Rect = self.hv_surf.get_rect(centerx = rect.centerx,
                                             top = 50)
        self.tg_surf: pygame.Surface = font.render('the game', True, title_color)
        self.tg_rect: pygame.Rect = self.tg_surf.get_rect(centerx = rect.centerx,
                                             bottom = rect.bottom - 50)
        font = pygame.font.Font(None, 32)
        self.pa_surf: pygame.Surface = font.render('Press any key', True, press_color)
        self.pa_rect: pygame.Rect = self.pa_surf.get_rect(centerx = rect.centerx,
                                             bottom = rect.bottom - 20)

    def event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.set_next('full_map')
        
    def update(self) -> None:
        if self.start_delay:
            self.start_delay -= 1
        else:
            self.logo_rect.x += self.logo_vel_x
            self.logo_rect.y += self.logo_vel_y
            self.rotation += self.logo_rot
            if self.logo_rect.centerx >= self.rect.centerx:
                self.logo_rect.centerx = self.rect.centerx
                self.logo_vel_x = 0
            if self.logo_rect.centery >= self.rect.centery:
                self.logo_rect.centery = self.rect.centery
                self.logo_vel_y = 0
            if (self.logo_vel_x == 0 and self.logo_vel_y == 0
                and self.rotation % 360 == 0):
                    self.logo_rot = 0

    def render(self, surface: pygame.Surface) -> None:
        if self.animate:
            if self.logo_rot == 0:
                surface.blit(self.logo, self.logo_rect)
                surface.blit(self.hv_surf, self.hv_rect)
                surface.blit(self.tg_surf, self.tg_rect)
                surface.blit(self.pa_surf, self.pa_rect)
                self.animate = False
            else:
                surface.fill(bg_color)
                rotated_logo = pygame.transform.rotate(self.logo, self.rotation)
                rotated_logo_rect = rotated_logo.get_rect(center=self.logo_rect.center)
                surface.blit(rotated_logo, rotated_logo_rect)
