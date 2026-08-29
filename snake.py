#!/usr/bin/env python3
"""Classic Snake, playable in the terminal. Arrow keys to move, q to quit."""

import curses
import random

RAINBOW = [
    curses.COLOR_RED,
    curses.COLOR_YELLOW,
    curses.COLOR_GREEN,
    curses.COLOR_CYAN,
    curses.COLOR_BLUE,
    curses.COLOR_MAGENTA,
]


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    curses.start_color()
    curses.use_default_colors()
    for i, color in enumerate(RAINBOW, start=1):
        curses.init_pair(i, color, -1)

    height, width = stdscr.getmaxyx()
    height -= 1
    width -= 1

    snake = [(height // 2, width // 4 + i) for i in range(3)][::-1]
    direction = (0, 1)
    food = (random.randint(1, height - 1), random.randint(1, width - 1))
    score = 0
    frame = 0

    while True:
        key = stdscr.getch()
        if key == ord("q"):
            break
        elif key == curses.KEY_UP and direction != (1, 0):
            direction = (-1, 0)
        elif key == curses.KEY_DOWN and direction != (-1, 0):
            direction = (1, 0)
        elif key == curses.KEY_LEFT and direction != (0, 1):
            direction = (0, -1)
        elif key == curses.KEY_RIGHT and direction != (0, -1):
            direction = (0, 1)

        head_y, head_x = snake[0]
        new_head = (head_y + direction[0], head_x + direction[1])

        if (
            new_head[0] <= 0 or new_head[0] >= height
            or new_head[1] <= 0 or new_head[1] >= width
            or new_head in snake
        ):
            break

        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            while True:
                food = (random.randint(1, height - 1), random.randint(1, width - 1))
                if food not in snake:
                    break
        else:
            snake.pop()

        stdscr.erase()
        stdscr.border()
        stdscr.addstr(0, 2, f" Score: {score} (q to quit) ")
        stdscr.addch(food[0], food[1], "•")
        for i, (y, x) in enumerate(snake):
            color = curses.color_pair((i + frame) % len(RAINBOW) + 1)
            stdscr.addch(y, x, "█" if i == 0 else "o", color)
        stdscr.refresh()
        frame += 1

    stdscr.nodelay(False)
    stdscr.erase()
    stdscr.addstr(height // 2, max(width // 2 - 10, 0), f"Game over! Score: {score}")
    stdscr.addstr(height // 2 + 1, max(width // 2 - 14, 0), "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
