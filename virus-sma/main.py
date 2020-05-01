#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from agent.hospital import Hospital
from agent.human import Human
from environnement.world import World


def generate_parser():
    parser = argparse.ArgumentParser(description="Set epidemy parameters.")
    parser.add_argument("size",
                        type=int,
                        help="The size of the world, this is a square")
    parser.add_argument("iter",
                        type=int,
                        help="Iteration number")
    parser.add_argument("hospitals",
                        type=int,
                        help="Number of hospitals on the map")
    parser.add_argument("humans",
                        type=int,
                        help="Number of humans on the map")
    parser.add_argument("sicks",
                        type=int,
                        help="Number of sick peopl among the human")
    parser.add_argument("--log",
                        action="store_true",
                        help="Log the execution in a log file")
    parser.add_argument('--verbose',
                        '-v',
                        action='count',
                        default=0)

    return parser


def main():
    parser = generate_parser()
    args = parser.parse_args()
    world = World(args.size, log=args.log, verbose=args.verbose)
    world.set_agents(hospitals=args.hospitals,
                     humans=args.humans,
                     sicks=args.sicks)
    world.start_simulation(max_iterations=args.iter)


if __name__ == "__main__":
    main()
