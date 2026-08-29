# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This folder contains small, standalone terminal games written in Python. There is no build system, package manifest, linter, or test suite — each script is self-contained and depends only on the Python standard library.

## Running the scripts

```bash
python3 game_of_life.py        # Conway's Game of Life, starts with a glider gun
python3 game_of_life.py random # start from a random grid instead
python3 snake.py               # Snake, playable with arrow keys, q to quit
```

`snake.py` uses `curses`, so it must be run in an actual terminal (not through a non-interactive shell).

## Structure

- `game_of_life.py` — animates Conway's Game of Life directly to stdout using ANSI escape codes for screen clearing; no external dependencies.
- `snake.py` — a `curses`-based Snake implementation; game state (snake body, direction, food, score) lives entirely in local variables inside `main()`.

Each file is independent; there is no shared code between them.


