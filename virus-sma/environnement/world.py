#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sys import exit
from random import randint, randrange, choice, random  # a remplacer
import logging

from environnement.world_statter import WorldStatter
from environnement.world_logger import WorldLogger
from agent.hospital import Hospital
from agent.human import Human


class World(WorldStatter, WorldLogger):
    SYMBOL_EMPTY = "."

    MAX_HOSPITALS = 0.10
    MAX_HUMANS = 0.5

    VIRUS_MORTALITY = 0.03
    MORTALITY_STATE = 10

    def __init__(self, size, log, verbose):
        # stats
        WorldStatter.__init__(self)

        # lgos
        WorldLogger.__init__(self, log, verbose)

        # map
        self._hospitals_position = []
        self._humans_position = []
        self._map = {}
        self._size = size
        for row in range(self._size):
            self._map[row] = {}
            for column in range(self._size):
                self._map[row][column] = None

        self.logger.debug("End of world's initialization.")

    @staticmethod
    def pause():
        print('Hit <enter> to continue...')
        input()

    def display(self):
        print('\033[2J')
        for row in range(self._size):
            print("\t", end="")
            for column in range(self._size):
                if self._map[row][column] is None:
                    print(self.SYMBOL_EMPTY, end="")
                else:
                    print(self._map[row][column], end="")
            print()

    def end_display(self):
        print("\033[2J")
        self.display_stats()

    def is_valid_position(self, row, column):
        res = row >= 0
        res = res and column >= 0
        res = res and row < self._size
        res = res and column < self._size

        return res

    def _is_agent(self, row, column, agent_type):
        res = self.is_valid_position(row, column)
        res = res and isinstance(self._map[row][column], agent_type)

        return res

    def is_hospital(self, row, column):
        return self._is_agent(row, column, Hospital)

    def is_human(self, row, column):
        return self._is_agent(row, column, Human)

    def is_empty(self, row, column):
        res = self.is_valid_position(row, column)
        res = res and self._map[row][column] is None

        return res

    def check_is_valid_world(self, hospitals, humans, sicks):
        max_hospitals = self._size**2 * self.MAX_HOSPITALS
        max_humans = self._size**2 * self.MAX_HUMANS
        hospitals_out_of_capacity = hospitals > max_hospitals
        humans_out_of_capacity = humans > max_humans
        too_many_sicks = sicks > humans
        oof_msg = "{}' quantity exceed maximum value allowed: {} > {} ({}% of the world)."
        if hospitals_out_of_capacity:
            print(oof_msg.format("Hospitals", hospitals, max_hospitals,
                                 self.MAX_HOSPITALS * 100))
        if humans_out_of_capacity:
            print(oof_msg.format("Humans", humans, max_humans,
                                 self.MAX_HUMANS * 100))
        if too_many_sicks:
            print(f"Sicks quantity exceed number of safe humans: {sicks} > {agents}")

        return hospitals_out_of_capacity or humans_out_of_capacity or too_many_sicks

    def get_free_coordinates(self):
        empty = False
        while not empty:
            x = randint(0, self._size - 1)
            y = randint(0, self._size - 1)
            empty = self.is_empty(x, y)

        return (x, y)

    def _add_agent(self, coordinates, agent_type, agents_position, msg=None):
        self._map[coordinates[0]][coordinates[1]] = agent_type()
        agents_position.append(coordinates)

        if msg is None:
            msg = "Agent in {}".format(coordinates)
        self.logger.info(msg)

    def contamine(self, human):
        human.contamine()
        self.update_stats("contamined")

    def heal(self, human):
        human.heal()
        self.update_stats("heal")

    def die(self, coordinates):
        human = self._map[coordinates[0]][coordinates[1]]
        human.die()
        self.update_stats("dead")
        self._humans_position.remove(coordinates)
        self._map[coordinates[0]][coordinates[1]] = None

    def _add_human(self, coordinates, is_sick=False):
        msg = "{} in {}".format("Human", coordinates)
        self._add_agent(coordinates, Human, self._humans_position, msg)
        self.update_stats("safe")
        if is_sick:
            self.logger.debug("Initial contamination")
            self.contamine(self._map[coordinates[0]][coordinates[1]])

    def _add_hospital(self, coordinates):
        msg = "{} in {}".format("Hospital", coordinates)
        self._add_agent(coordinates, Hospital, self._hospitals_position, msg)

    def set_agents(self, hospitals, humans, sicks):
        self.logger.debug("Filling the grid...")
        msg = "*" * 4 + " INITIALIZATION " + "*" * 4 + ""
        self.logger.info(msg)
        is_ko = self.check_is_valid_world(hospitals, humans, sicks)
        if is_ko:
            exit(1)
        else:
            for i in range(humans - sicks):
                self.logger.debug("New healthy human: {}".format(i))
                coordinates = self.get_free_coordinates()
                self._add_human(coordinates, False)
            for i in range(sicks):
                self.logger.debug("New sick human: {}".format(i))
                coordinates = self.get_free_coordinates()
                self._add_human(coordinates, True)
            for i in range(hospitals):
                self.logger.debug("New hospital: {}".format(i))
                coordinates = self.get_free_coordinates()
                self._add_hospital(coordinates)

    def get_neighborhood(self, coordinates):
        left = coordinates[0] - 1, coordinates[1]
        right = coordinates[0] + 1, coordinates[1]
        up = coordinates[0], coordinates[1] - 1
        down = coordinates[0], coordinates[1] + 1

        return (left, right, up, down)

    def _propagate(self):
        for position in self._humans_position:
            our_guy = self._map[position[0]][position[1]]
            if our_guy.was_already_sick():
                neighborhood = self.get_neighborhood(position)
                for neighbor_position in neighborhood:
                    if self.is_human(*neighbor_position):
                        neighbor = self._map[neighbor_position[0]][neighbor_position[1]]
                        if not (neighbor.is_sick() or neighbor.is_immune()):
                            self.contamine(neighbor)
                    elif self.is_hospital(*neighbor_position):
                        self.heal(our_guy)

    def _increment(self):
        for position in self._humans_position:
            our_guy = self._map[position[0]][position[1]]
            our_guy.increment_state()
            if our_guy.is_sick() and our_guy.get_state() == World.MORTALITY_STATE:
                if random() <= World.VIRUS_MORTALITY:
                    self.die(position)
                else:
                    self.heal(our_guy)

    def _move_humans(self):
        i = 0
        while i < len(self._humans_position):
            position = self._humans_position[i]
            neighborhood = [j for j in self.get_neighborhood(position) if self.is_valid_position(*j) and self.is_empty(*j)]
            if neighborhood:
                rand_ind = randrange(len(neighborhood))
                new_position = neighborhood[rand_ind]
                self._humans_position[i] = new_position
                self._map[new_position[0]][new_position[1]] = self._map[position[0]][position[1]]
                self._map[position[0]][position[1]] = None
            i += 1

    def _next_iteration(self):
        self._iteration += 1
        msg = f"**** Iteration #{self._iteration} ****"
        self.logger.info(msg)
        self._increment()
        self._propagate()
        self._move_humans()

    def start_simulation(self, max_iterations):
        self.logger.debug("Launch of the simulation")
        iteration = 0
        while self._humans_position and iteration < max_iterations:
            self.logger.debug("New iteration")
            self.display()
            iteration += 1
            World.pause()
            self._next_iteration()
        if iteration == max_iterations:
            self.logger.info(f"[STOP] Maximum iterations reached ({max_iterations})")
        else:
            self.logger.info("[STOP] No more human in the simulation!")

        self.end_display()
        self.logger.debug("End of the simulation")



if __name__ == "__main__":
    print("Hello world!")
