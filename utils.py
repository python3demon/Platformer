import pygame
import json

def load_map(file_name: str = "level_data.json") -> dict[int, dict]:
    clear_map: dict[int, dict] = {}

    try:
        with open(file_name, "r") as file:
            level_map = json.load(file)
    except FileNotFoundError:
        clear_map = {
            1: {
                "floor": [[0, 320], [64, 320], [128, 320], [192, 320], [256, 320], [320, 320], [384, 320], [448, 320]], 
                "lava": [[256, 320]]
            }
        }
    else:
        for key, value in level_map.items():
            clear_map[int(key)] = value

    return clear_map

def import_map(platform: list, level: int, file_name: str = "level_data.json") -> None:
    """Сохраняет отредактированную карту под номер level"""
    level_map: dict[int, dict] = load_map()
    level_map[level] = {"floor":[], "lava":[]}

    for block in platform:
        if block.type_block == "floor":
            level_map[level]["floor"].append(block.rect.topleft)
        elif block.type_block == "lava":
            level_map[level]["lava"].append(block.rect.topleft)
    
    with open(file_name, "w") as file:
        json.dump(level_map, file)

def load_img(img_path: str, resize: tuple[int, int] | None = None) -> pygame.Surface:
    img: pygame.Surface = pygame.image.load(img_path).convert_alpha()

    if resize is not None:
        img: pygame.Surface = pygame.transform.scale(img, resize)

    return img

def middle(width: int, height: int, width2: int, height2: int) -> tuple[int, int]:
    return (width//2-width2//2, height//2-height2//2)

def get_img_text(
        text: str,
        font_color: tuple[int, int, int] | str | None = None,
        font_antialias: bool = True,
        font_text: str | None = None,
        font_size: int = 36
    ) -> pygame.Surface:

    color: tuple[int, int, int] | str | None = font_color if font_color else (255, 0, 0)
    font: pygame.font.Font = pygame.font.Font(font_text, font_size)
    text_surface: pygame.Surface = font.render(text, font_antialias, color)
    
    return text_surface

def output(
    screen: pygame.Surface,
    text: str,
    x: int | str,
    y: int | str,
    font_color: tuple[int, int, int] | str | None = None,
    font_antialias: bool = True,
    font_text: str | None = None,
    font_size: int = 36,
    width: int = 832,
    height: int = 640,
) -> None:
    text_surface = get_img_text(text, font_color, font_antialias, font_text, font_size)
    if x == "сenter":
        x = width // 2 - text_surface.get_width() // 2
    if y == "сenter":
        y = height // 2 - text_surface.get_height() // 2
    screen.blit(text_surface, (x, y))
