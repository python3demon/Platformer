from __future__ import annotations

import pygame

from config import Context, GameConfig
from scenes import Menu
from state_manager import StateManager

pygame.init()


class Game:
    def __init__(self) -> None:
        self.game_config = GameConfig()
        self.width, self.height = self.game_config.window["size"]
        self.caption = self.game_config.window["caption"]
        self.fps = self.game_config.window["fps"]
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()

        self.context = Context(self.game_config)
        self.state_manager = StateManager()
        self.state_manager.push(Menu(self.state_manager, self.context))

        self.running = True

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.state_manager.handle_event(event)

            self.state_manager.update()
            self.state_manager.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
