# -*- coding: utf-8 -*-
import argparse
import random
import sys


WIDTH, HEIGHT = 1000, 1000
NUMPOINTS = 10000
RADIUS = 10  # adjust radius depending on size and number of points
RANDOM_SEED = 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Wygeneruj pseudolosowe dane i przekieruj do pliku.
10000 punktów o srednicy 1-10 na obszarze 1000x1000.
Jako argument mozna podac random seed jako integer.""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    seed = RANDOM_SEED
    if len(sys.argv) > 1:
        seed = int(sys.argv[1])
    # Seeded random setup
    random.seed(seed)  # Use same seed for reproducibility
    points = [
        (random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, RADIUS))
        for _ in range(NUMPOINTS)
    ]

    print(len(points))
    for p in points:
        print(p[0], p[1], p[2])

    # Fake start and end_point
    print(random.randint(1, WIDTH - 1), random.randint(1, HEIGHT - 1))
    print(0, 0)
