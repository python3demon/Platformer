from __future__ import annotations
from typing import Callable
from state_manager import StateManager, State
from config import Context

import pygame
import classes
import utils

class Menu(State):
    def __init__(self, manager: StateManager, context: Context) -> None:
        super().__init__(manager, context)
        self.margin: int = 25
        self.background: pygame.Surface = utils.load_img("assets/back_menu.png")
        self.buttons: pygame.sprite.Group[classes.MenuButton] = pygame.sprite.Group()
        self.buttons_config: list[tuple[str, Callable]] = [
            ("start", lambda: self.manager.push(LevelsMenu(self.manager, self.context))),
            ("settings", lambda: self.manager.push(SettingsMenu(self.manager, self.context))),
            ("Exit", lambda: self.manager.pop())
        ]

        size_window: tuple[int, int] = self.context.game_config.width, self.context.game_config.height
        size_button: tuple[int, int] = self.context.size_menu_button
        y_offset: int = -(size_button[1] + self.margin)
        for button in self.buttons_config:
            self.buttons.add(classes.MenuButton(
                (size_window[0] // 2 - size_button[0] // 2,
                size_window[1] // 2 - size_button[1] // 2 + y_offset),
                *button
            ))
            y_offset += size_button[1] + self.margin

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.func()

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))
        self.buttons.draw(screen)

class LevelsMenu(State):
    def __init__(self, manager: StateManager, context: Context) -> None:
        super().__init__(manager, context)
        self.margin_levels_x = 100
        self.buttons_levels = pygame.sprite.Group()
        
        for key in self.context.map_levels.keys():
            self.buttons_levels.add(
                classes.LevelButton(
                    (self.margin_levels_x*int(key), 100),
                    key,
                    lambda k=key: self.manager.push(Gameplay(self.manager, self.context, k))
                )
            )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.manager.pop()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons_levels:
                if button.rect.collidepoint(event.pos):
                    button.func()
                    break

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        self.buttons_levels.draw(screen)
                
class Gameplay(State):
    def __init__(self, manager: StateManager, context: Context, level: str) -> None:
        super().__init__(manager, context)
        self.level = level
        self.sky = utils.load_img("assets/sky.png")
        self.platform = pygame.sprite.Group()
        self.player = classes.Player("danil", "assets/danil.png", (0,0))
        self.load_level()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.manager.pop()
            elif event.key == pygame.K_RETURN and self.context.root:
                utils.import_map(self.platform.sprites(), self.level)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.context.root:
            x, y = event.pos
            x = x // 64 * 64
            y = y // 64 * 64

            if event.button == 1:
                self.platform.add(classes.Floor((x, y)))
            elif event.button == 2:
                all_floors = self.platform.sprites()
                if all_floors:
                    last_block = all_floors[-1]
                    self.platform.remove(last_block)
            else:
                self.platform.add(classes.Lava((x, y)))

    def load_level(self) -> None:
        level_map = self.context.map_levels[self.level]
        floors = level_map["floor"]
        lavas = level_map["lava"] 
        for floor in floors:
            self.platform.add(classes.Floor(floor))
        for lava in lavas:
            self.platform.add(classes.Lava(lava))

    def update(self) -> None:
        if self.player.rect.top >= self.context.game_config.height:
            self.player.reset()
        self.player.update(self.platform)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.sky, (0, 0))
        self.platform.draw(screen)
        screen.blit(self.player.image, self.player.rect)

class SettingsMenu(State):
    def __init__(self, manager: StateManager, context: Context) -> None:
        super().__init__(manager, context)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.manager.pop()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        utils.output(screen, "В разработке...", x="сenter", y="сenter", font_color="green")
