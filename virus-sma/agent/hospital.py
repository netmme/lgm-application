#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from agent.agent import Agent


class Hospital(Agent):
    SYMBOL = "H"

    def __init__(self):
        self._symbol = self.SYMBOL


if __name__ == "__main__":
    print("Hello world!")
