import pygame

from typing import Optional, Type

from screens.setup import (SCREEN_SIZE, fps_color, fps_border_color,
                           transition_color, fps_font, transparent)
from screens.level_base import LevelBase
from screens.start import Start
from screens.end import End
from screens.full_map import FullMap
from screens.maxim import Maxim
from screens.marconi import Marconi
from screens.tesla import Tesla
from screens.tickets import Tickets
from screens.forum1 import Forum1
from screens.forum2 import Forum2
from screens.forum3 import Forum3
from screens.forum4 import Forum4
from screens.forum5 import Forum5
from screens.tent import Tent
from screens.hertz import Hertz
from screens.volta import Volta
from screens.campers import Campers
from screens.testing import Testing
from screens.emcomm import Emcomm
from screens.flea_market import FleaMarket
from screens.food import Food


class Main:
    screens: dict[str, Type[LevelBase]] = {
        'start': Start,
        'end'  : End,
        'full_map': FullMap,
        'maxim' : Maxim,
        'marconi': Marconi,
        'tesla': Tesla,
        'tickets': Tickets,
        'forum1': Forum1,
        'forum2': Forum2,
        'forum3': Forum3,
        'forum4': Forum4,
        'forum5': Forum5,
        'tent': Tent,
        'hertz': Hertz,
        'volta': Volta,
        'campers': Campers,
        'testing': Testing,
        'emcomm': Emcomm,
        'flea_market': FleaMarket,
        'food': Food,
    }
    
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Hamvention® the game')
        self.screen: pygame.Surface = pygame.display.set_mode(SCREEN_SIZE)
        self.screen_rect: pygame.Rect = self.screen.get_rect()
        self.display: pygame.Surface = pygame.Surface(SCREEN_SIZE)
        self.display_transition: pygame.Surface = pygame.Surface(SCREEN_SIZE)

        self.transition: int = 60     # 0 open, 60 closed
        self.transition_vel: int = -1 # 1 close, -1 open, 0 n/c

        self.controller: LevelBase = LevelBase(self.screen_rect, self.set_next)
        self.next_controller: LevelBase | None = None

        self.fps: int = 0
        fps_size: tuple[int, int] = fps_font.size('00')
        self.fps_border_surf: pygame.Surface = pygame.Surface((fps_size[0] + 20,
                                              fps_size[1] + 4))
        self.fps_border_surf.set_colorkey(transparent)
        self.fps_border_rect: pygame.Rect = self.fps_border_surf.get_rect()
        pygame.draw.rect(self.fps_border_surf,
                         fps_border_color,
                         self.fps_border_rect,
                         border_radius=8)
        self.fps_border_rect.right = SCREEN_SIZE[0] - 4
        self.fps_border_rect.bottom = SCREEN_SIZE[1] - 4

        self.fps_surf: pygame.Surface = fps_font.render('', True, fps_color)
        self.fps_rect: pygame.Rect = self.fps_surf.get_rect(center=self.fps_border_rect.center)
        self.fps_timer: int = pygame.event.custom_type()

        self.set_next('start')
        
        pygame.time.set_timer(self.fps_timer, 1000)
        

    def set_next(self, name: Optional[str]) -> None:
        if name is None:
            self.next_controller = None
        else:
            self.next_controller = self.screens[name](self.screen_rect,
                                                      self.set_next)
        self.transition_vel = 1

    def update_fps(self) -> None:
        self.fps_surf = fps_font.render(f'{self.fps:2}', True, fps_color)
        self.fps_rect = self.fps_surf.get_rect(center=self.fps_border_rect.center)
        self.fps = 0
        
    def event_loop(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # self.running = False
                self.set_next(None)
            elif event.type == self.fps_timer:
                self.update_fps()
            else:
                self.controller.event(event)
                
    def update(self) -> None:
        self.controller.update()
        self.fps += 1
        if self.transition_vel:
            self.transition += self.transition_vel
            if self.transition <= 0:
                self.transition_vel = 0
            if self.transition >= 60:
                self.transition_vel = -1
                if self.next_controller:
                    self.controller = self.next_controller
                else:
                    self.running = False
                
    def render(self) -> None:
        self.controller.render(self.display)
        self.display_transition.blit(self.display, self.screen_rect)

        if self.transition_vel:
            transition_surf = self.display.copy()
            transition_surf.fill(transition_color)
            pygame.draw.circle(transition_surf, (c := (255,255,255)),
                (transition_surf.get_width() // 2,
                 transition_surf.get_height() // 2),
                 (60 - self.transition) * 8)
            transition_surf.set_colorkey(c)
            self.display_transition.blit(transition_surf, (0,0))
            
        self.display_transition.blit(self.fps_border_surf,
                                     self.fps_border_rect)
        self.display_transition.blit(self.fps_surf,
                                     self.fps_rect)            
        self.screen.blit(self.display_transition, self.screen_rect)

    def run(self) -> None:
        clock: pygame.time.Clock = pygame.time.Clock()
        self.running = True
        while self.running:
            self.event_loop()
            self.update()
            self.render()
            pygame.display.flip()
            clock.tick(30)
        pygame.quit()

            
if __name__ == '__main__':
    Main().run()
