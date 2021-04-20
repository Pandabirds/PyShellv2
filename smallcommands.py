import time
import datetime
import curses
import sys
import os
import threading

import superglobals
import screenfunctions

class Stopwatch:
    def __init__(self, name, seconds_until_alarm):
        self.name = name
        self.seconds = seconds_until_alarm

class Timer:
    def __init__(self, name, minutes_until_alarm, booleans):
        self.name = name
        self.seconds = time.perf_counter() + minutes_until_alarm * 60
        self.minutes_until_alarm = minutes_until_alarm
        self.bits = 0b0
        # Converts the booleans into bits.
        for i, boolean in enumerate(booleans):
            self.bits += boolean << i

class Countdown:
    def __init__(self, name, hour, minute, booleans):
        cur_hour = datetime.datetime.today().hour
        cur_min = datetime.datetime.today().minute
        cur_sec = datetime.datetime.today().second
        self.name = name
        self.seconds = time.perf_counter() + \
        ((hour - cur_hour) * 3600) + ((minute - cur_min) * 60) - cur_sec
        self.bits = 0b0
        # Converts the booleans into bits.
        for i, boolean in enumerate(booleans):
            self.bits += boolean << i

def stopwatch_command(cmds):
    try:
        cmds[1] = cmds[1].lower()
        if cmds[1] == "new":
            if screenfunctions.indexists(cmds, 2):

                superglobals.stopwatch_list.append(Stopwatch(cmds[2],
                time.perf_counter()))
                
                return 0

            superglobals.stopwatch_list.append(Stopwatch(
            f"stopwatch {len(superglobals.stopwatch_list)}", time.perf_counter()))

        if cmds[1] in ["remove", "del"] and screenfunctions.indexists(cmds, 2):
            del superglobals.stopwatch_list[int(cmds[2])]
        if cmds[1] == "reset" and screenfunctions.indexists(cmds, 2):
            superglobals.stopwatch_list[int(cmds[2])].seconds = time.perf_counter()
        return 0
    except Exception:
        pass

def timer_command(cmds):
    try:
        cmds[1] = cmds[1].lower()
        if cmds[1] == "new" and screenfunctions.indexists(cmds, 2):
            if screenfunctions.indexists(cmds, 3):

                superglobals.timer_list.append(Timer(cmds[3], float(cmds[2]),
                (True,)))
                return 0

            superglobals.timer_list.append(Timer(
            f"timer {len(superglobals.timer_list) + 1}", float(cmds[2]),
            (True,)))

        if cmds[1] in ["remove", "del"] and screenfunctions.indexists(cmds, 2):
            del superglobals.timer_list[int(cmds[2])]
        if cmds[1] == "reset" and screenfunctions.indexists(cmds, 2):
            superglobals.timer_list[int(cmds[2])].seconds = \
            time.perf_counter() + \
            superglobals.timer_list[int(cmds[2])].minutes_until_alarm
        return 0
    except Exception:
        pass

def countdown_command(cmds):
    # cmds[1] is new/del
    # cmds[2] is hours
    # cmds[3] is minutes
    # cmds[4] is name
    try:
        cmds[1] = cmds[1].lower()
        if cmds[1] == "new" and screenfunctions.indexists(cmds, 2, 3):
            if screenfunctions.indexists(cmds, 4):
                superglobals.countdown_list.append(Countdown(cmds[4],
                int(cmds[2]), int(cmds[3]), (True,)))
                return 0
            superglobals.countdown_list.append(Countdown(
            f"countdown {len(superglobals.countdown_list)}",
            int(cmds[2]), int(cmds[3]), (True,)))
        if cmds[1] in ["remove", "del"] and screenfunctions.indexists(cmds, 2):
            del superglobals.countdown_list[int(cmds[2])]
        return 0
    except Exception:
        pass

def color_command(stdscr, cmds):
    old_dir = os.getcwd()
    os.chdir(os.path.dirname(sys.argv[0]))

    if screenfunctions.is_int(cmds[1]) and int(cmds[1]) < 256:
        with open("pyshelldata.txt", "w") as file:
            file.write(f"color: {cmds[1]}")
        curses.init_pair(1, int(cmds[1]), -1)
        stdscr.attron(curses.color_pair(1))

    if cmds[1] in ["default", "reset"]:
        with open("pyshelldata.txt", "w") as file:
            file.write("color: 225")
        curses.init_pair(1, 225, -1)
        stdscr.attron(curses.color_pair(1))

    os.chdir(old_dir)