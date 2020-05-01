#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from agent.agent import Agent


class Human(Agent):
    SYMBOL = "O"
    SYMBOL_SICK = "K"
    SYMBOL_IMMUNE = "I"

    def __init__(self):
        self._state = -1
        self._immune = False
        self._dead = False

    def is_sick(self):
        return self._state != -1 and not self._immune

    def was_already_sick(self):
        return self.is_sick() and self._state != 0

    def is_immune(self):
        return self._immune

    def contamine(self):
        self._state = 0

    def heal(self):
        self._immune = True

    def die(self):
        self._dead = True

    def increment_state(self):
        if self.is_sick():
            self._state += 1

    def get_state(self):
        return self._state

    def __str__(self):
        if self.is_sick():
            return self.SYMBOL_SICK
        elif self.is_immune():
            return self.SYMBOL_IMMUNE
        else:
            return self.SYMBOL


if __name__ == "__main__":
    print("Hello world!")
