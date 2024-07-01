# -*- coding: utf-8 -*-
import argparse
from quadnode import QuadNode
from helper import find_connected_transmitters
from transmitter import Transmitter


WIDTH, HEIGHT = 1000, 1000
NODE_CAPACITY = 4


RESPONSE_TRUE = "bezpieczny przelot jest możliwy"
RESPONSE_FALSE = "bezpieczny przelot nie jest możliwy"


def main():
    parser = argparse.ArgumentParser(
        description="""Znajdź trasę dla drona poprzez znalezienie sąsiednich nadajników.
Wprowadź dane ręcznie lub przekieruj standardowy input z pliku:
    python main.py < input_task.txt""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-g', '--game',
        action='store_true',
        help='''Wizualizacja z pygame. Wymaga biblioteki pygame: pip install pygame
Uruchom test:
    python main.py --game < input_random.txt
Wygeneruj pseudolosowe dane z generate_random_input.py
        '''
    )

    args = parser.parse_args()

    # Input start
    number_of_transmitters = int(input())

    transmitter_input = []
    for _ in range(number_of_transmitters):
        input_line = input()
        transmitter_input.append(tuple(int(number) for number in input_line.split()))

    start_point = tuple(int(number) for number in input().split())
    start_point = Transmitter(start_point[0], start_point[1], 0)

    end_point = tuple(int(number) for number in input().split())
    end_point = Transmitter(end_point[0], end_point[1], 0)
    # Input end

    # Calculate map size
    transmitters = []
    max_x, max_y, max_r = 0, 0, 0
    for t in transmitter_input:
        max_x = t[0] if t[0] > max_x else max_x
        max_y = t[1]if t[1] > max_y else max_y
        max_r = t[2] if t[2] > max_r else max_r
        transmitters.append(Transmitter(*t))

    size = min((max(max_x, max_y) + max_r), max(WIDTH, HEIGHT))
    scale = min(WIDTH // size, HEIGHT // size)

    transmitters.append(end_point)  # add end_point to the list of transmitters

    # Build quadtree
    root = QuadNode(0, 0, size, size, NODE_CAPACITY)
    for transmitter in transmitters:
        root.insert(root, transmitter, 0, 0, size, size)

    start_point.connect()
    traversed_transmitters = set()
    find_connected_transmitters(
        root,
        [start_point],
        traversed_transmitters,
        max_r
    )

    if end_point.connected:
        print(RESPONSE_TRUE)
    else:
        print(RESPONSE_FALSE)

    if args.game:
        from gametest import Game
        game = Game(root, transmitters, start_point, end_point, WIDTH, HEIGHT, max_r, scale)
        game.start()


if __name__ == '__main__':
    main()
