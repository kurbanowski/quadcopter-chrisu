# Quadcopter Route Finder

This project is a tool to find a route for a drone by identifying neighboring transmitters. You can input the data manually or redirect the standard input from a file.

## Table of Contents

- [Installation](#Installation)
- [Usage](#Usage)
- [Arguments](#Arguments)
- [Generating Random Input](#generating-random-input)
- [Visualization](#Visualization)

## Installation

Before using the tool, ensure you have Python installed on your system. Additionally, if you plan to use the visualization feature, you need to install the `pygame` library:

```bash
pip install pygame
```

## Usage

You can run the main script with either manual input or by redirecting input from a file:

```bash
python main.py < input_task.txt
```
Output returns string informing if there is a route connecting start_point and end_point.

## Arguments

-g, --game: Enables visualization with pygame. Requires the pygame library.
Click on transmitter nodes to highlight all connections with green.
Example usage:

```bash
python main.py --game < input_rand.txt
```

## Generating Random Input

You can generate pseudo-random data and redirect it to a file. This generates 10,000 points with diameters ranging from 1 to 10 on a 1000x1000 area. Optionally, you can provide a random seed as an integer argument.

## Example script to generate input data:

```bash
python 0 generate_random_input.py > input_random.txt
```

## Visualization

To visualize the drone route finding process, you can enable the visualization mode using the --game argument. This will display a graphical representation using pygame.

# Example usage:

```bash
python main.py --game < input_random.txt
```

This feature requires the pygame library. Install it using:

```bash
pip install pygame
```

