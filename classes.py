from __future__ import annotations

import pygame

from utils import get_img_text, load_img, middle


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        path: str,
        pos: tuple[int, int],
        text: str,
        font_color: tuple[int, int, int] | str | None = None,
        font_antialias: bool = True,
        font_text: str | None = None,
        font_size: int = 36,
    ):
        super().__init__()

        self.image = load_img(path).copy()
        self.rect = pygame.Rect(*pos, *self.image.get_size())
        self.text = text

        color = font_color if font_color else (255, 0, 0)
        text_image = get_img_text(
            self.text, color, font_antialias, font_text, font_size
        )
        text_pos: tuple[int, int] = middle(*self.rect.size, *text_image.get_size())

        self.image.blit(text_image, text_pos)


class Block(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], type_block: str):
        super().__init__()
        self.type_block = type_block
        self.image = load_img(f"assets/{type_block}.png")
        self.rect = pygame.Rect(*pos, *self.image.get_size())


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
        resize: tuple[int, int] = (48, 96),
    ):
        super().__init__()
        self.name = name
        self.left_sprite = load_img(path_to_img, resize)
        self.right_sprite = pygame.transform.flip(self.left_sprite, True, False)
        self.image = self.left_sprite
        self.rect = pygame.Rect(*pos, *self.image.get_size())
        self.speed_x = 6
        self.velocity_x = 0  # текущая скорость по оси X
        self.velocity_y = 0  # текущая скорость по оси Y
        self.gravity = 1
        self.jump_power = -14
        self.can_jump = True

    def reset(self):
        self.rect.left = 0
        self.rect.bottom = 100

    def hits_lava(self, lava: pygame.sprite.Group):
        if pygame.sprite.spritecollide(self, lava, False):
            return True
        return False

    def update(self, platform: pygame.sprite.Group):
        floor = pygame.sprite.Group()
        lava = pygame.sprite.Group()

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
