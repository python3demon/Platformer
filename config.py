import utils

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
        self.map_levels = utils.load_map()
        self.skin = "danil"
        self.root = True
        self.size_menu_button = (270, 80)
        self.size_level_button = (60, 60)

    def set_skin(self, skin_name: str) -> None:
        self.skin = skin_name
