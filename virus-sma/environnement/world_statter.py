#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from random import randint, choice, random  # a remplacer


class WorldStatter():
    def __init__(self):
        self._iteration = 0
        self._stats = {
            "dead": 0,
            "contamined": 0,
            "recovered": 0,
            "safe": 0
        }

    def update_stats(self, state):
        if state == "heal":
            self._stats["contamined"] -= 1
            self._stats["recovered"] += 1
        elif state == "dead":
            self._stats["contamined"] -= 1
            self._stats["dead"] += 1
        elif state == "contamined":
            self._stats["safe"] -= 1
            self._stats["contamined"] += 1
        elif state == "safe":
            self._stats["safe"] += 1

    def display_stats(self):
        print("*" * 8, "STASTICS", "*" * 8)
        print(f"* Safe: {self._stats['safe']:<10}")
        print(f"* Contamined: {self._stats['contamined']:<10}")
        print(f"* Recovered: {self._stats['recovered']:<10}")
        print(f"* Dead: {self._stats['dead']:<10}")
