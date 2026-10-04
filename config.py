import json
from pathlib import Path

import map_utils


class GameConfig:
    def __init__(self, config_path="config.json"):
        self.config_path = Path(config_path)
        self.read_config()

    def read_config(self):
        if not self.config_path.exists():
            self._create_config()

        with open(self.config_path, "r", encoding="utf-8") as file:
            config = json.load(file)

        self.window = config["window"]
        self.imgs = config["imgs"]
        self.block = config["block"]
        self.settings = config["settings"]

    def _create_config(self):
        base_config = {
            "window": {"size": [832, 640], "caption": "My Platformer", "fps": 60},
            "imgs": {
                "default_skin": "assets/danil.png",
                "background_menu_img": "assets/back_menu.png",
                "background_game_img": "assets/sky.png",
                "buttons": {"menu": "assets/rectangle.png", "rect": "assets/rect.png"},
            },
            "block": {
                "solids": {"floor": "assets/floor.png"},
                "triggers": {"lava": "assets/lava.png"},
            },
            "settings": {
                "can_edit_map": True,
            },
        }
        with open(self.config_path, "w", encoding="utf-8") as file:
            json.dump(base_config, file)


class Context:
    def __init__(self, game_config: GameConfig):
        """Контекст игры, здесь хранится все данные текущего сеанса"""
        self.game_config: GameConfig = game_config
        self.map_levels = map_utils.load_map()
        self.current_skin = self.game_config.imgs["default_skin"]
        self.root = self.game_config.settings["can_edit_map"]

    def set_skin(self, skin_name: str) -> None:
        self.skin = skin_name
