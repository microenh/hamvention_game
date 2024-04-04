from typing import Callable, Optional
import pygame

from .level_base import LevelBase

end_color = pygame.Color('darkred')
text_color = pygame.Color('red')

class Forum4(LevelBase):

    def __init__(self, rect: pygame.Rect,
                       set_next : Callable[[Optional[str]], None]) -> None:
        super().__init__(rect, set_next)
        self.local: Optional[pygame.Surface] = None
   
    def event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.set_next('full_map' if event.key == pygame.K_r else None)
    
    def render(self, surface: pygame.Surface) -> None:
        if self.local is None:
            self.local = surface.copy()
            self.local.fill(end_color)
            font = pygame.font.Font(None, 96)
            text_surf = font.render('Forum 4', True, text_color)
            text_rect = text_surf.get_rect(center = self.rect.center)
            self.local.blit(text_surf, text_rect)
            font = pygame.font.Font(None, 32)
            text_surf = font.render('Press any other key to end', True, text_color)
            text_rect = text_surf.get_rect(centerx = self.rect.centerx,
                                           bottom = self.rect.bottom - 20)
            self.local.blit(text_surf, text_rect)
            text_surf = font.render('Press R to restart', True, text_color)
            text_rect = text_surf.get_rect(centerx = self.rect.centerx,
                                           bottom = text_rect.top - 2)
            self.local.blit(text_surf, text_rect)
            
        surface.blit(self.local, self.rect)
