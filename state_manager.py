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
    
    @staticmethod
    def check_stack(func):
        def wrapper(self, *args, **kwargs):
            if self.stack_state:
                return func(self, *args, **kwargs)
        return wrapper

    def push(self, state: State) -> None:
        self.stack_state.append(state)

    @check_stack
    def pop(self) -> None:
        self.stack_state.pop()
    
    @check_stack
    def handle_event(self, event: pygame.event.Event) -> None:
        self.stack_state[-1].handle_event(event)
    
    @check_stack
    def update(self) -> None:
        self.stack_state[-1].update()
    
    @check_stack
    def draw(self, screen: pygame.Surface) -> None:
        self.stack_state[-1].draw(screen)
