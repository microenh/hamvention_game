from __future__ import annotations
import pygame

from typing import Callable, Optional

class LevelBase:
    def __init__(self, rect: pygame.Rect,
                 set_next: Callable[[Optional[str]], None]) -> None:
        self.rect: pygame.Rect = rect
        self.set_next: Callable[[Optional[str]], None] = set_next

    def event(self, _: pygame.event.Event) -> None:
        pass

    def update(self) -> None:
        pass

    def render(self, _: pygame.Surface) -> None:
        pass
    
