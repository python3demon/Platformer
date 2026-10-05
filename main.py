from __future__ import annotations

import pygame

from config import Context, GameConfig
from scenes import Menu
from state_manager import StateManager

pygame.init()


class Game:
    def __init__(self) -> None:
        self.game_config = GameConfig()
        self.screen = pygame.display.set_mode(
            (self.game_config.WIDTH, self.game_config.HEIGHT)
        )
        self.game_config.init_paths()
        pygame.display.set_caption(self.game_config.CAPTION)

        self.context = Context(self.game_config)
        self.state_manager = StateManager()
        self.state_manager.push(Menu(self.state_manager, self.context))

    def run(self) -> None:
        self.clock = pygame.time.Clock()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.state_manager.handle_event(event)

            self.state_manager.update()
            self.state_manager.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(self.game_config.FPS)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
