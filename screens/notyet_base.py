from typing import Callable, Optional
import pygame

from .level_base import LevelBase
from .setup import (notyet_color, notyet_text_color,
                    notyet_font, notyet_press_font)

class NotYetBase(LevelBase):

    def __init__(self, rect: pygame.Rect,
                       set_next : Callable[[Optional[str]], None],
                 title: str) -> None:
        super().__init__(rect, set_next)
        self.local: Optional[pygame.Surface] = None
        self.title = title
   
    def event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.set_next('full_map' if event.key == pygame.K_e else None)
    
    def render(self, surface: pygame.Surface) -> None:
        if self.local is None:
            self.local = surface.copy()
            self.local.fill(notyet_color)
            text_surf = notyet_font.render(self.title, True, notyet_text_color)
            text_rect = text_surf.get_rect(center = self.rect.center)
            self.local.blit(text_surf, text_rect)
            text_surf = notyet_press_font.render('Press any other key to end', True, notyet_text_color)
            text_rect = text_surf.get_rect(centerx = self.rect.centerx,
                                           bottom = self.rect.bottom - 20)
            self.local.blit(text_surf, text_rect)
            text_surf = notyet_press_font.render('Press E to exit', True, notyet_text_color)
            text_rect = text_surf.get_rect(centerx = self.rect.centerx,
                                           bottom = text_rect.top - 2)
            self.local.blit(text_surf, text_rect)
            
        surface.blit(self.local, self.rect)
