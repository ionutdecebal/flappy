#!/usr/bin/env python3
import curses
import random
import time

FRAME_TIME = 0.05
GRAVITY = 0.7
FLAP_VELOCITY = -4.0
PIPE_GAP = 6
PIPE_DISTANCE = 18
PIPE_WIDTH = 3

BIRD_X = 10


def draw_centered(stdscr, y, text):
    height, width = stdscr.getmaxyx()
    x = max(0, (width - len(text)) // 2)
    stdscr.addstr(y, x, text[: max(0, width - 1)])


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    stdscr.timeout(0)

    height, width = stdscr.getmaxyx()
    ground_y = height - 2

    bird_y = height // 2
    velocity = 0.0

    pipes = []
    score = 0
    ticks = 0
    alive = True

    def spawn_pipe(x_pos):
        gap_top = random.randint(3, max(3, ground_y - PIPE_GAP - 3))
        pipes.append({"x": x_pos, "gap_top": gap_top})

    spawn_pipe(width + 10)

    while True:
        start_time = time.time()
        stdscr.erase()
        height, width = stdscr.getmaxyx()
        ground_y = height - 2

        key = stdscr.getch()
        if key in (ord("q"), ord("Q")):
            break
        if key in (ord(" "), ord("w"), ord("W"), curses.KEY_UP):
            if alive:
                velocity = FLAP_VELOCITY
            elif key in (ord(" "), ord("w"), ord("W"), curses.KEY_UP):
                alive = True
                bird_y = height // 2
                velocity = 0.0
                pipes.clear()
                score = 0
                ticks = 0
                spawn_pipe(width + 10)

        if alive:
            velocity += GRAVITY
            bird_y += velocity
            ticks += 1

            if ticks % PIPE_DISTANCE == 0:
                spawn_pipe(width + PIPE_DISTANCE)

            for pipe in pipes:
                pipe["x"] -= 1

            pipes = [pipe for pipe in pipes if pipe["x"] + PIPE_WIDTH > 0]

            for pipe in pipes:
                if pipe["x"] + PIPE_WIDTH == BIRD_X:
                    score += 1

            if bird_y < 1 or bird_y >= ground_y:
                alive = False

            for pipe in pipes:
                in_pipe_x = pipe["x"] <= BIRD_X < pipe["x"] + PIPE_WIDTH
                in_gap = pipe["gap_top"] <= int(bird_y) < pipe["gap_top"] + PIPE_GAP
                if in_pipe_x and not in_gap:
                    alive = False

        for pipe in pipes:
            x = pipe["x"]
            if 0 <= x < width:
                for dy in range(1, ground_y):
                    in_gap = pipe["gap_top"] <= dy < pipe["gap_top"] + PIPE_GAP
                    if not in_gap:
                        for w in range(PIPE_WIDTH):
                            if 0 <= x + w < width:
                                stdscr.addch(dy, x + w, "|")

        for x in range(width):
            stdscr.addch(ground_y, x, "=")

        if 0 <= int(bird_y) < ground_y:
            stdscr.addch(int(bird_y), BIRD_X, "@")

        draw_centered(stdscr, 0, "Flappy Terminal - Space/W to flap, Q to quit")
        stdscr.addstr(1, 2, f"Score: {score}")

        if not alive:
            draw_centered(stdscr, height // 2, "Game Over! Press Space/W to restart")

        stdscr.refresh()
        elapsed = time.time() - start_time
        time.sleep(max(0, FRAME_TIME - elapsed))


if __name__ == "__main__":
    curses.wrapper(main)
