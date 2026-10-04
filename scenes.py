from __future__ import annotations

import pygame

import classes
import map_utils
import utils
from config import Context
from state_manager import State, StateManager


class Menu(State):
    def __init__(self, manager: StateManager, context: Context) -> None:
        super().__init__(manager, context)
        self.init_buttons()

    def init_buttons(self):
        btn_path = self.context.game_config.imgs["buttons"]["menu"]
        bg = self.context.game_config.imgs["background_menu_img"]
        btn_size = pygame.image.load(btn_path).get_size()
        window_size = self.context.game_config.window["size"]
        text_color = (0, 168, 120)
        pos = (100, 100)
        margin = 25

        self.background = utils.load_img(bg)
        self.buttons = pygame.sprite.Group()

        center_pos = utils.middle(
            window_size[0], window_size[1], btn_size[0], btn_size[1]
        )

        start = classes.Button(btn_path, pos, "start", text_color)
        settings = classes.Button(btn_path, pos, "settings", text_color)
        shop = classes.Button(btn_path, pos, "shop", text_color)

        start.rect.left, start.rect.top = center_pos
        start.rect.top = start.rect.top - start.rect.height - margin
        settings.rect.left, settings.rect.top = center_pos

        shop.rect.left, shop.rect.top = center_pos
        shop.rect.top = shop.rect.top + shop.rect.height + margin

        self.buttons.add(start, settings, shop)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    if button.text == "start":
                        self.manager.push(LevelsMenu(self.manager, self.context))
                    elif button.text == "settings":
                        self.manager.push(SettingsMenu(self.manager, self.context))
                    elif button.text == "shop":
                        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))
        self.buttons.draw(screen)


class LevelsMenu(State):
    def __init__(self, manager: StateManager, context: Context):
        super().__init__(manager, context)
        self.init_buttons()

    def init_buttons(self):
        btn_path = self.context.game_config.imgs["buttons"]["level"]

        margin_levels_x: int = 100
        self.buttons_levels: pygame.sprite.Group = pygame.sprite.Group()
        for key in self.context.map_levels:
            self.buttons_levels.add(
                classes.Button(btn_path, (margin_levels_x * key, 100), str(key))
            )

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.manager.pop()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons_levels:
                if button.rect.collidepoint(event.pos):
                    self.manager.push(
                        Gameplay(self.manager, self.context, int(button.text))
                    )

    def draw(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        self.buttons_levels.draw(screen)


class Gameplay(State):
    def __init__(self, manager: StateManager, context: Context, level: int):
        super().__init__(manager, context)
        self.level = level
        self.sky = utils.load_img(self.context.game_config.imgs["background_game_img"])
        self.platform: pygame.sprite.Group = pygame.sprite.Group()
        self.player = classes.Player(
            self.context.current_skin.split("/")[1], self.context.current_skin, (0, 0)
        )
        self.load_level()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.manager.pop()
            elif event.key == pygame.K_RETURN and self.context.root:
                map_utils.import_map(self.platform.sprites(), self.level)
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

    def load_level(self):
        level_map = self.context.map_levels[self.level]
        floors = level_map["floor"]
        lavas = level_map["lava"]
        for floor in floors:
            self.platform.add(classes.Floor(floor))
        for lava in lavas:
            self.platform.add(classes.Lava(lava))

    def update(self):
        if self.player.rect.top >= self.context.game_config.window["size"][1]:
            self.player.reset()
        self.player.update(self.platform)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.sky, (0, 0))
        self.platform.draw(screen)
        screen.blit(self.player.image, self.player.rect)


class SettingsMenu(State):
    def __init__(self, manager: StateManager, context: Context):
        super().__init__(manager, context)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.manager.pop()

    def draw(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        utils.output(
            screen, "В разработке...", x="сenter", y="сenter", font_color="green"
        )
