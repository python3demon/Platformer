from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from config import Context


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
