import map_utils

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
        self.map_levels: dict = map_utils.load_map()
        self.skin: str = "danil"
        self.root: bool = True

    def set_skin(self, skin_name: str) -> None:
        self.skin = skin_name
