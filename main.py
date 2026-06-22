import pygame
import utils
import classes

pygame.init()
width, height = 832, 640

class GameState:
    def __init__(self, game_self):
        self.game_self = game_self
        self.next_state = None
    
    def handle_event(self, event): pass
    def update(self): pass
    def draw(self, screen): pass

class Menu(GameState):
    def __init__(self, game_self):
        super().__init__(game_self)
        self.margin = 25
        self.background = utils.load_img("assets/back_menu.png")
        self.buttons = pygame.sprite.Group()
        senter_pos = utils.middle(self.game_self.width, self.game_self.height, 270, 80) # Для кнопок типо rectangle размер всегда 270x80

        self.start_button = classes.Button("rectangle", (100, 100), "start", font_size=36, font_color=(0, 168, 120))
        self.start_button.rect.left, self.start_button.rect.top = senter_pos
        self.start_button.rect.top = self.start_button.rect.top - self.start_button.rect.height - self.margin
 
        self.settings_button = classes.Button("rectangle", (100, 100), "settings", font_size=36, font_color=(0, 168, 120))
        self.settings_button.rect.left, self.settings_button.rect.top = senter_pos

        self.exit_button = classes.Button("rectangle", (100, 100), "EXIT", font_size=36, font_color=(0, 168, 120))
        self.exit_button.rect.left, self.exit_button.rect.top = senter_pos
        self.exit_button.rect.top = self.exit_button.rect.top + self.exit_button.rect.height + self.margin

        self.buttons.add(self.start_button, self.settings_button, self.exit_button)
 
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    if button.text == "start":
                        self.next_state = "levels"
                    elif button.text == "settings":
                        self.next_state = "settings"
                    elif button.text == "EXIT":
                        self.game_self.running = False # Тушим главный цикл напрямую!
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.buttons.draw(screen)

class LevelsMenu(GameState):
    def __init__(self, game_self):
        super().__init__(game_self)
        self.margin_levels_x = 100
        self.buttons_levels = pygame.sprite.Group()
        for key in self.game_self.map_levels.keys():
            self.buttons_levels.add(classes.Button("rect", (self.margin_levels_x*key, 100), str(key)))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game_self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.next_state = "menu"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons_levels:
                if button.rect.collidepoint(event.pos):
                    self.game_self.platform.empty()
                    self.game_self.proris_map = False
                    self.game_self.level = int(button.text)
                    self.game_self.player.reset()
                    self.next_state = "game"

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.buttons_levels.draw(screen)
                
class Gameplay(GameState):
    def __init__(self, game_self):
        super().__init__(game_self)
        self.sky = utils.load_img("assets/sky.png")
        self.level_map = self.game_self.map_levels[self.game_self.level]

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game_self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.next_state = "levels"
            elif event.key == pygame.K_RETURN and self.game_self.root:
                utils.import_map(self.game_self.platform.sprites(), self.game_self.level)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.game_self.root:
            x, y = event.pos
            x = x // 64 * 64
            y = y // 64 * 64

            if event.button == 1:
                self.game_self.platform.add(classes.Floor((x, y)))
            elif event.button == 2:
                all_floors = self.game_self.platform.sprites()
                last_block = all_floors[-1]
                self.game_self.platform.remove(last_block)
            else:
                self.game_self.platform.add(classes.Lava((x, y)))

    def update(self):
        if self.game_self.proris_map is False:
            self.level_map = self.game_self.map_levels[self.game_self.level]
            floors = self.level_map["floor"]
            lavas = self.level_map["lava"] 
            for floor in floors:
                self.game_self.platform.add(classes.Floor(floor))
            for lava in lavas:
                self.game_self.platform.add(classes.Lava(lava))
            self.game_self.proris_map = True

        if self.game_self.player.rect.top >= self.game_self.height:
            self.game_self.player.reset()

    def draw(self, screen):
        screen.blit(self.sky, (0, 0))
        self.game_self.platform.draw(screen)
        self.game_self.player.update(self.game_self.platform)
        screen.blit(self.game_self.player.image, self.game_self.player.rect)

class SettingsMenu(GameState):
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game_self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.next_state = "menu"
    def draw(self, screen):
        screen.fill((0, 0, 0))
        utils.output(screen, "В разработке...", x="senter", y="senter", font_color="green")

class Game:
    def __init__(self, width, height, FPS, caption):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.caption = caption
        pygame.display.set_caption(self.caption)
        self.FPS = FPS
        self.clock = pygame.time.Clock()

        # GAMESTATE
        self.player = classes.Player("danil", "assets/danil.png", (0, 0))
        self.platform = pygame.sprite.Group()
        self.map_levels = utils.load_map()
        self.root = True
        self.proris_map = False

        self.level = 1
        self.states = {
            "menu": Menu(self),
            "levels": LevelsMenu(self),
            "settings": SettingsMenu(self),        
            "game":  Gameplay(self),
        }

        self.current_state = self.states["menu"]
        self.running = True

    def change_state(self):
        if self.current_state.next_state is not None:
            next_state_name = self.current_state.next_state
            self.current_state.next_state = None
            self.current_state = self.states[next_state_name]
    
    def run(self):
        while self.running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_state.handle_event(event)
            
            self.current_state.update()
            self.change_state()
            self.current_state.draw(self.screen)
           
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    game = Game(width=width, height=height, FPS=60, caption="My Platformer")
    game.run()
