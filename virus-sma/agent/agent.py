#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Agent():
    def __init__(self):
        self._symbol = ''
        self._position = (0, 0)

    def get_position(self):
        return self._position

    def get_position_row(self):
        return self._position[0]

    def get_position_column(self):
        return self._position[1]

    def set_position(self, row, column):
        self._position = (row, column)

    def __str__(self):
        return self._symbol


if __name__ == "__main__":
    print("Hello world!")
    agent = Agent()
