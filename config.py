import json
from os import path
from pathlib import Path

import map_utils
from utils import load_img


class GameConfig:
    def __init__(self, config_path="config.json"):
        self.config_path = Path(config_path)
        self.WIDTH = 832
        self.HEIGHT = 640
        self.CAPTION = "My Platformer"
        self.FPS = 60
        self.read_config()

    def init_paths(self):
        self.PATHS = {
            "bg_menu": load_img(path.join("assets", "back_menu.png")),
            "bg_game": load_img(path.join("assets", "sky.png")),
            "skins": {"danil": load_img(path.join("assets", "danil.png"))},
            "btn_menu": load_img(path.join("assets", "rectangle.png")),
            "btn_level": load_img(path.join("assets", "rect.png")),
            "blocks": {
                "solids": {
                    "block_floor": load_img(path.join("assets", "floor.png")),
                },
                "triggers": {
                    "block_lava": load_img(path.join("assets", "lava.png")),
                },
            },
        }
        self.DEFAULT_SKIN = {"name": "danil", "image": self.PATHS["skins"]["danil"]}

    def read_config(self):
        if not self.config_path.exists():
            self._create_config()

        with open(self.config_path, "r", encoding="utf-8") as file:
            config = json.load(file)

        self.window = config["window"]
        self.settings = config["settings"]

    def _create_config(self):
        base_config = {"window": {"fps": 60}, "settings": {"can_edit_map": True}}
        with open(self.config_path, "w", encoding="utf-8") as file:
            json.dump(base_config, file)


class Context:
    def __init__(self, game_config: GameConfig):
        """Контекст игры, здесь хранится все данные текущего сеанса"""
        self.game_config: GameConfig = game_config
        self.map_levels = map_utils.load_map()
        self._current_skin = self.game_config.DEFAULT_SKIN
        self.root = self.game_config.settings["can_edit_map"]

    @property
    def current_skin(self) -> dict:
        return self._current_skin

    @current_skin.setter
    def current_skin(self, name_skin: str):
        surface_skin = self.game_config.PATHS["skins"].get(name_skin)
        if not surface_skin:
            raise ValueError(f"Скин '{name_skin}' не найден в конфигурации игры!")
        self._current_skin = {
            "name": f"{name_skin}",
            "image": self.game_config.PATHS["skins"][name_skin],
        }
