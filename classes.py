from __future__ import annotations
from collections.abc import Callable
import pygame
from utils import load_img, get_img_text, middle

class Button(pygame.sprite.Sprite):
    def __init__(
            self,
            type_button: str,
            pos: tuple[int, int],
            text: str,
            func: Callable,
            font_color: tuple[int, int, int] | str| None = None,
            font_antialias: bool = True,
            font_text: str | None = None,
            font_size: int = 36
        ) -> None:
        super().__init__()
        self.pos = pos
        self.text = text
        self.func = func

        self.image: pygame.Surface = load_img(f"assets/{type_button}.png")
        self.rect: pygame.Rect = pygame.Rect(*pos, *self.image.get_size())

        text_image: pygame.Surface = get_img_text(self.text, font_color, font_antialias, font_text, font_size)
        text_pos: tuple[int, int] = middle(*self.rect.size, *text_image.get_size())

        # Наносит текст на поверхность картинки кнопки (в памяти, не на экране)
        self.image.blit(text_image, text_pos)
        
class MenuButton(Button):
    def __init__(
            self,
            pos: tuple[int, int],
            text: str,
            func: Callable,
            font_color: tuple[int, int, int] | str| None = (0, 168, 120),
            font_antialias: bool = True,
            font_text: str | None = None,
            font_size: int = 36
        ) -> None:
        super().__init__("rectangle", pos, text, func, font_color, font_antialias, font_text, font_size)

class LevelButton(Button):
    def __init__(
            self,
            pos: tuple[int, int],
            text: str,
            func: Callable,
            font_color: tuple[int, int, int] | str| None = None,
            font_antialias: bool = True,
            font_text: str | None = None,
            font_size: int = 36
        ) -> None:
        super().__init__("rect", pos, text, func, font_color, font_antialias, font_text, font_size)

class Block(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], type_block: str) -> None:
        super().__init__()
        self.type_block: str = type_block
        self.image: pygame.Surface = load_img(f"assets/{type_block}.png")
        self.rect: pygame.Rect = pygame.Rect(*pos, *self.image.get_size())

class Floor(Block):
    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__(pos, "floor")

class Lava(Block):
    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__(pos, "lava")
        

class Player(pygame.sprite.Sprite):
    def __init__(
            self,
            name: str,
            path_to_img: str,
            pos: tuple[int, int],
            resize: tuple[int, int] = (48, 96)
        ) -> None:
        super().__init__()
        self.name: str = name
        self.left_sprite: pygame.Surface = load_img(path_to_img, resize)
        self.right_sprite: pygame.Surface = pygame.transform.flip(self.left_sprite, True, False)
        self.image: pygame.Surface = self.left_sprite
        self.rect: pygame.Rect = pygame.Rect(*pos, *self.image.get_size())
        self.speed_x: int = 6
        self.velocity_x: int = 0 # текущая скорость по оси X
        self.velocity_y: int = 0 # текущая скорость по оси Y
        self.gravity: int = 1
        self.jump_power: int = -14
        self.can_jump: bool = True

    def reset(self) -> None:
        self.rect.left = 0
        self.rect.bottom = 100

    def hits_lava(self, lava: pygame.sprite.Group) -> bool:
        if pygame.sprite.spritecollide(self, lava, False):
            return True
        return False

    def update(self, platform: pygame.sprite.Group) -> None:
        floor: pygame.sprite.Group = pygame.sprite.Group()
        lava: pygame.sprite.Group = pygame.sprite.Group()

        for block in platform:
            if block.type_block == "floor":
                floor.add(block)
            else:
                lava.add(block)
                
        keys = pygame.key.get_pressed()

        self.velocity_x = 0
      
        if keys[pygame.K_d]:
            self.image = self.right_sprite
            self.velocity_x = self.speed_x

        if keys[pygame.K_a]:
            self.image = self.left_sprite
            self.velocity_x = -self.speed_x
        
        self.rect.left += self.velocity_x


        if self.hits_lava(lava):
            self.reset()
            return
        
        hits_x_floor = pygame.sprite.spritecollide(self, floor, False)

        for block in hits_x_floor:
            if block.rect.top >= self.rect.bottom - self.gravity:
                continue
            elif self.velocity_x > 0:
                self.rect.right = block.rect.left
            elif self.velocity_x < 0:
                self.rect.left = block.rect.right
        
        # РАБОТА С ОСЬЮ Y
        if keys[pygame.K_w] and self.can_jump:
            self.velocity_y = self.jump_power

        self.velocity_y += self.gravity
        self.rect.bottom += self.velocity_y

        if self.hits_lava(lava):
            self.reset()
            return

        self.can_jump = False
        hits_y_floor = pygame.sprite.spritecollide(self, floor, False)

        for block in hits_y_floor:
            if self.velocity_y > 0:
                self.rect.bottom = block.rect.top
                self.velocity_y = 0
                self.can_jump = True
            elif self.velocity_y < 0:
                self.rect.top = block.rect.bottom
                self.velocity_y = 0