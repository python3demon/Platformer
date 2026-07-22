from __future__ import annotations
import pygame
from config import GameConfig, Context
from state_manager import StateManager
from scenes import Menu

pygame.init()

class Game:
    def __init__(self) -> None:
        self.game_config: GameConfig = GameConfig()
        self.width: int = self.game_config.width
        self.height: int = self.game_config.height
        self.caption: str = self.game_config.caption
        self.fps: int = self.game_config.fps
        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)
        self.clock: pygame.time.Clock = pygame.time.Clock()        

        self.context: Context = Context(self.game_config)
        self.state_manager: StateManager = StateManager()
        self.state_manager.push(Menu(self.state_manager, self.context))

        self.running: bool = True

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or len(self.state_manager.stack_state) == 0:
                    self.running = False
                self.state_manager.handle_event(event)

            self.state_manager.update()
            self.state_manager.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = Game()
    game.run()
