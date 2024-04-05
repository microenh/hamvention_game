from typing import Callable, Optional
import pygame

from .level_base import LevelBase
from .setup import end_color, text_color, title_font, text_font


class End(LevelBase):

    def __init__(self, rect: pygame.Rect,
                       set_next : Callable[[Optional[str]], None]) -> None:
        super().__init__(rect, set_next)
        self.local: Optional[pygame.Surface] = None
   
    def event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.set_next('start' if event.key == pygame.K_r else None)
    
    def render(self, surface: pygame.Surface) -> None:
        if self.local is None:
            self.local = surface.copy()
            self.local.fill(end_color)
            text_surf: pygame.Surface = title_font.render('The End', True, text_color)
            text_rect: pygame.Rect = text_surf.get_rect(center = self.rect.center)
            self.local.blit(text_surf, text_rect)
            text_surf = text_font.render('Press any other key to end', True, text_color)
            text_rect = text_surf.get_rect(centerx = self.rect.centerx,
                                           bottom = self.rect.bottom - 20)
            self.local.blit(text_surf, text_rect)
            text_surf = text_font.render('Press R to restart', True, text_color)
            text_rect = text_surf.get_rect(centerx = self.rect.centerx,
                                           bottom = text_rect.top - 2)
            self.local.blit(text_surf, text_rect)
            
        surface.blit(self.local, self.rect)
