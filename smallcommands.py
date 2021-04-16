import time
import datetime
import curses
import screenfunctions
import sys
import superglobals
import threading

def stopwatch_command(cmds):
    try:
        cmds[1] = cmds[1].lower()
        if cmds[1] == "new":
            if screenfunctions.indexists(cmds, 2):
                superglobals.stopwatch_list.append((cmds[2],
                time.perf_counter()))
                return 0
            superglobals.stopwatch_list.append(
            (f"stopwatch {len(superglobals.stopwatch_list) + 1}",
            time.perf_counter()))
        if (cmds[1] == "remove" or cmds[1] == "del") \
        and screenfunctions.indexists(cmds, 2):
            del superglobals.stopwatch_list[int(cmds[2]) - 1]
    except Exception:
        pass

def timer_command(cmds):
    try:
        cmds[1] = cmds[1].lower()
        if cmds[1] == "new" and screenfunctions.indexists(cmds, 2):
            if screenfunctions.indexists(cmds, 3):
                superglobals.timer_list.append([cmds[3],
                time.perf_counter() + int(cmds[2]) * 60, True, False])
                return 0
            superglobals.timer_list.append(
            [f"timer {len(superglobals.timer_list) + 1}",
            time.perf_counter() + int(cmds[2]) * 60, True, False])
        if (cmds[1] == "remove" or cmds[1] == "del") \
        and screenfunctions.indexists(cmds, 2):
            del superglobals.timer_list[int(cmds[2]) - 1]
    except Exception:
        pass

def countdown_command(cmds):
    # cmds[1] is new/del
    # cmds[2] is hours
    # cmds[3] is minutes
    # cmds[4] is name
    cur_hour = datetime.datetime.today().hour
    cur_min = datetime.datetime.today().minute
    cur_sec = datetime.datetime.today().second
    try:
        cmds[1] = cmds[1].lower()
        if cmds[1] == "new" and screenfunctions.indexists(cmds, 2, 3):
            if screenfunctions.indexists(cmds, 4):
                superglobals.countdown_list.append([cmds[4],
                time.perf_counter() + ((int(cmds[2]) - cur_hour) * 3600) + ((int(cmds[3]) - cur_min) * 60) - cur_sec, True])
                return 0
            superglobals.countdown_list.append(
            [f"countdown {len(superglobals.countdown_list) + 1}",
            time.perf_counter() + ((int(cmds[2]) - cur_hour) * 3600) + ((int(cmds[3]) - cur_min) * 60) - cur_sec, True])
        if (cmds[1] == "remove" or cmds[1] == "del") \
        and screenfunctions.indexists(cmds, 2):
            del superglobals.countdown_list[int(cmds[2]) - 1]
    except Exception:
            curses.flash()
            curses.beep()