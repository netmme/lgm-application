#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
from logging.handlers import RotatingFileHandler


class WorldLogger():
    def __init__(self, log, verbose=0):
        # log
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        verbose_level = (5 - verbose) * 10
        self.stream_hand = logging.StreamHandler()
        self.stream_hand.setLevel(verbose_level)
        self.stream_hand.setFormatter(formatter)
        self.logger.addHandler(self.stream_hand)

        if log:
            self.file_hand = RotatingFileHandler("data/sma-virus.log", "a", 10**6, 1)
            self.file_hand.setLevel(logging.INFO)
            self.file_hand.setFormatter(formatter)
            self.logger.addHandler(self.file_hand)
