from typing import Callable, Optional
import pygame

from .notyet_base import NotYetBase

class Forum3(NotYetBase):

    def __init__(self, rect: pygame.Rect,
                       set_next : Callable[[Optional[str]], None]) -> None:
        super().__init__(rect, set_next, 'Forum 3')
