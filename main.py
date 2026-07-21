from __future__ import annotations
import pygame
import classes
import utils

pygame.init()
WIDTH, HEIGHT = 832, 640
CAPTION = "My Platformer"
FPS = 60

class GameConfig:
    def __init__(self) -> None:
        self.width: int = WIDTH
        self.height: int = HEIGHT
        self.caption: str = CAPTION
        self.fps: int = FPS

class Context:
    def __init__(self, game_config: GameConfig) -> None:
        """Контекст игры, здесь хранится все данные текущего сеанса"""
        self.game_config: GameConfig = game_config
        self.map_levels: dict = utils.load_map()
        self.skin: str = "danil"
        self.root: bool = True

    def set_skin(self, skin_name: str) -> None:
        self.skin = skin_name


class State:
    def __init__(self, manager: StateManager, context: Context) -> None:
        """Абстрактный класс который опписывает атрибуты Всех существующих сцен"""
        self.manager: StateManager = manager
        self.context: Context = context

    def handle_event(self, event: pygame.event.Event) -> None: 
        pass

    def update(self) -> None: 
        pass

    def draw(self, screen: pygame.Surface) -> None: 
        pass

class StateManager:
    def __init__(self) -> None:
        self.stack_state: list[State] = []
 
    def push(self, state: State) -> None:
        self.stack_state.append(state)

    def pop(self) -> None:
        if len(self.stack_state) > 1:
            self.stack_state.pop()
    
    def handle_event(self, event: pygame.event.Event) -> None:
        self.stack_state[-1].handle_event(event)
    
    def update(self) -> None:
        self.stack_state[-1].update()
    
    def draw(self, screen: pygame.Surface) -> None:
        self.stack_state[-1].draw(screen)


class Menu(State):
    def __init__(self, manager: StateManager, context: Context) -> None:
        super().__init__(manager, context)
        self.margin: int = 25
        self.background: pygame.Surface = utils.load_img("assets/back_menu.png")
        self.buttons: pygame.sprite.Group = pygame.sprite.Group()
        center_pos = utils.middle(self.context.game_config.width, self.context.game_config.height, 270, 80) 

        self.start_button = classes.Button("rectangle", (100, 100), "start", font_size=36, font_color=(0, 168, 120))
        self.start_button.rect.left, self.start_button.rect.top = center_pos
        self.start_button.rect.top = self.start_button.rect.top - self.start_button.rect.height - self.margin
 
        self.settings_button = classes.Button("rectangle", (100, 100), "settings", font_size=36, font_color=(0, 168, 120))
        self.settings_button.rect.left, self.settings_button.rect.top = center_pos

        self.exit_button = classes.Button("rectangle", (100, 100), "Shop", font_size=36, font_color=(0, 168, 120))
        self.exit_button.rect.left, self.exit_button.rect.top = center_pos
        self.exit_button.rect.top = self.exit_button.rect.top + self.exit_button.rect.height + self.margin

        self.buttons.add(self.start_button, self.settings_button, self.exit_button)
 
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    if button.text == "start":
                        self.manager.push(LevelsMenu(self.manager, self.context))
                    elif button.text == "settings":
                        self.manager.push(SettingsMenu(self.manager, self.context))
                    elif button.text == "Shop":
                        pass
    
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))
        self.buttons.draw(screen)

class LevelsMenu(State):
    def __init__(self, manager: StateManager, context: Context) -> None:
        super().__init__(manager, context)
        self.margin_levels_x: int = 100
        self.buttons_levels: pygame.sprite.Group = pygame.sprite.Group()
        for key in self.context.map_levels.keys():
            self.buttons_levels.add(classes.Button("rect", (self.margin_levels_x*key, 100), str(key)))

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.manager.pop()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons_levels:
                if button.rect.collidepoint(event.pos):
                    self.manager.push(Gameplay(self.manager, self.context, int(button.text)))

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((0, 0, 0))
        self.buttons_levels.draw(screen)
                
class Gameplay(State):
    def __init__(self, manager: StateManager, context: Context, level: int) -> None:
        super().__init__(manager, context)
        self.level: int = level
        self.sky: pygame.Surface = utils.load_img("assets/sky.png")
        self.platform: pygame.sprite.Group = pygame.sprite.Group()
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
