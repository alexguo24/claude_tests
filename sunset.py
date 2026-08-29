#!/usr/bin/env python3
"""Animates a sun setting over the ocean, drawn with ANSI true-color blocks."""

import math
import random
import sys
import time

WIDTH, HEIGHT = 84, 32
HORIZON = 20
SUN_X = WIDTH * 0.72
FRAMES = 48
ASPECT = 2.0  # terminal cells are ~2x taller than wide; squashes circles round

SKY_TOP = [(60, 90, 160), (95, 55, 105), (20, 16, 42)]
SKY_HORIZON = [(255, 205, 125), (255, 120, 70), (105, 40, 55)]
WATER_NEAR = [(255, 195, 135), (215, 95, 75), (55, 32, 55)]
WATER_FAR = [(30, 60, 110), (32, 24, 55), (8, 8, 22)]
SUN_BRIGHT = (255, 235, 150)
SUN_DIM = (225, 70, 40)
MOUNTAIN = (18, 16, 34)

STARS = [(x, y, random.random()) for _ in range(40)
         for x in [random.randint(0, WIDTH - 1)]
         for y in [random.randint(0, HORIZON - 2)]]


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


def keyframe_color(stops, t):
    if t <= 0.5:
        return lerp_color(stops[0], stops[1], t / 0.5)
    return lerp_color(stops[1], stops[2], (t - 0.5) / 0.5)


def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))


def mountain_height(x):
    return max(0, int(3 + 2.2 * math.sin(x * 0.28) + 1.4 * math.sin(x * 0.11 + 1.3)))


def cell_color(x, y, t, frame):
    sun_y = lerp(HORIZON - 11, HORIZON + 4, t)
    sun_color = lerp_color(SUN_BRIGHT, SUN_DIM, t)
    radius = 4.5

    if y < HORIZON:
        base = lerp_color(keyframe_color(SKY_TOP, t), keyframe_color(SKY_HORIZON, t),
                           y / (HORIZON - 1))
        dx, dy = x - SUN_X, y - sun_y
        dist = math.sqrt(dx * dx + (dy * ASPECT) ** 2)
        if dist <= radius:
            edge = dist / radius
            return lerp_color(sun_color, lerp_color(sun_color, (150, 40, 25), 0.5), edge ** 2)
        if dist <= radius + 2.5:
            glow = 1 - (dist - radius) / 2.5
            base = lerp_color(base, sun_color, glow * 0.5)

        if x < WIDTH * 0.4:
            h = mountain_height(x)
            if y >= HORIZON - h:
                haze = 0.15 + 0.1 * t
                return lerp_color(MOUNTAIN, base, haze)

        if t > 0.55:
            for sx, sy, phase in STARS:
                if sx == x and sy == y:
                    twinkle = 0.5 + 0.5 * math.sin(frame * 0.3 + phase * 10)
                    strength = min(1.0, (t - 0.55) / 0.3) * twinkle
                    return lerp_color(base, (255, 255, 255), strength)
        return base

    depth = (y - HORIZON) / (HEIGHT - 1 - HORIZON)
    base = lerp_color(keyframe_color(WATER_NEAR, t), keyframe_color(WATER_FAR, t), depth)
    ripple = math.sin(x * 0.4 + y * 0.3 + frame * 0.5) * 10 * (1 - depth)
    base = tuple(clamp(c + ripple) for c in base)

    mirror_y = 2 * HORIZON - sun_y
    wobble = math.sin(y * 0.6 + frame * 0.4) * 1.6
    dx, dy = (x - SUN_X - wobble), (y - mirror_y)
    dist = math.sqrt(dx * dx + (dy * ASPECT) ** 2)
    band_radius = radius * (1 - depth * 0.5)
    if dist <= band_radius and (x + y + frame) % 3 != 0:
        return lerp_color(base, sun_color, 0.55)
    return base


def render(frame):
    t = frame / (FRAMES - 1)
    lines = []
    for y in range(HEIGHT):
        row = []
        last = None
        for x in range(WIDTH):
            color = cell_color(x, y, t, frame)
            if color != last:
                row.append(f"\033[48;2;{color[0]};{color[1]};{color[2]}m")
                last = color
            row.append(" ")
        lines.append("".join(row) + "\033[0m")
    sys.stdout.write("\033[H\033[J" + "\n".join(lines) + "\n")
    sys.stdout.flush()


def main():
    try:
        for frame in range(FRAMES):
            render(frame)
            time.sleep(0.08)
    except KeyboardInterrupt:
        pass
    sys.stdout.write("\033[?25h")
    print("\nThe sun has set.")


if __name__ == "__main__":
    main()
