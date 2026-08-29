#!/usr/bin/env python3
"""Conway's Game of Life, animated in the terminal."""

import os
import random
import sys
import time

WIDTH, HEIGHT = 60, 30

GLIDER_GUN = [
    (1, 25), (2, 23), (2, 25), (3, 13), (3, 14), (3, 21), (3, 22), (3, 35), (3, 36),
    (4, 12), (4, 16), (4, 21), (4, 22), (4, 35), (4, 36), (5, 1), (5, 2), (5, 11),
    (5, 17), (5, 21), (5, 22), (6, 1), (6, 2), (6, 11), (6, 15), (6, 17), (6, 18),
    (6, 23), (6, 25), (7, 11), (7, 17), (7, 25), (8, 12), (8, 16), (9, 13), (9, 14),
]


def new_grid(random_fill=False):
    grid = [[0] * WIDTH for _ in range(HEIGHT)]
    if random_fill:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                grid[y][x] = random.choice([0, 0, 0, 1])
    else:
        for y, x in GLIDER_GUN:
            if y < HEIGHT and x < WIDTH:
                grid[y][x] = 1
    return grid


def step(grid):
    new = [[0] * WIDTH for _ in range(HEIGHT)]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            alive_neighbors = sum(
                grid[(y + dy) % HEIGHT][(x + dx) % WIDTH]
                for dy in (-1, 0, 1)
                for dx in (-1, 0, 1)
                if (dy, dx) != (0, 0)
            )
            if grid[y][x] and alive_neighbors in (2, 3):
                new[y][x] = 1
            elif not grid[y][x] and alive_neighbors == 3:
                new[y][x] = 1
    return new


def render(grid, generation):
    lines = [f"Generation {generation}  (Ctrl+C to stop)"]
    for row in grid:
        lines.append("".join("█" if cell else " " for cell in row))
    sys.stdout.write("\033[H\033[J" + "\n".join(lines) + "\n")
    sys.stdout.flush()


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "gun"
    grid = new_grid(random_fill=(mode == "random"))
    generation = 0
    try:
        while True:
            render(grid, generation)
            grid = step(grid)
            generation += 1
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
