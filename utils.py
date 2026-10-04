import pygame

_IMAGE_CACHE = {}


def load_img(img_path: str, resize: tuple[int, int] | None = None) -> pygame.Surface:
    key = f"{img_path}_{resize}"
    if key not in _IMAGE_CACHE:
        img: pygame.Surface = pygame.image.load(img_path).convert_alpha()
        if resize:
            img = pygame.transform.scale(img, resize)
        _IMAGE_CACHE[key] = img

    return _IMAGE_CACHE[key]


def middle(width: int, height: int, width2: int, height2: int) -> tuple[int, int]:
    return (width // 2 - width2 // 2, height // 2 - height2 // 2)


def get_img_text(
    text: str,
    font_color: tuple[int, int, int] | str | None = None,
    font_antialias: bool = True,
    font_text: str | None = None,
    font_size: int = 36,
) -> pygame.Surface:

    color: tuple[int, int, int] | str | None = font_color if font_color else (255, 0, 0)
    font = pygame.font.Font(font_text, font_size)
    text_surface = font.render(text, font_antialias, color)

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
