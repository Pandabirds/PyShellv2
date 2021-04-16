import curses
import threading
import superglobals
import screenfunctions
import time
import datetime

def main(stdscr):
    stdscr.timeout(0)
    curses.noecho()
    curses.curs_set(False)

    max_y = stdscr.getmaxyx()[0] - 1
    max_x = stdscr.getmaxyx()[1] - 1

    def resizing_thread_function():
        while True:
            if max_y < 39 or max_x < 159:
                print("\x1b[8;40;160t")



    resizing_thread = threading.Thread(target=resizing_thread_function,
    daemon=True)
    resizing_thread.start()

    k = 0
    while k != ord('q'):

        max_y = stdscr.getmaxyx()[0] - 1
        max_x = stdscr.getmaxyx()[1] - 1

        stdscr.erase()
        screenfunctions.render_defaults(stdscr)
        stdscr.addstr(0, 45, str(datetime.datetime.now()))
        stopwatch_list = superglobals.stopwatch_list
        timer_list = superglobals.timer_list            
        countdown_list = superglobals.countdown_list
        if not (len(stopwatch_list) > int(max_y/2) or len(timer_list) > int(max_y/2)):
            for i in range(0, max_y + 1):
                stdscr.addstr(i, 98, "｜")
                stdscr.addstr(int(max_y / 2), 45, "─" * (max_x - 45))
            for i, stopwatch in enumerate(stopwatch_list):
                stdscr.addstr(i + 1, 100,
                f"{stopwatch[0]} : {round(time.perf_counter() - stopwatch[1], 2)} : {round((time.perf_counter() - stopwatch[1]) / 60, 2)} : {round((time.perf_counter() - stopwatch[1]) / 3600, 2)}")
            for i, timer in enumerate(timer_list):
                stdscr.addstr(i + 2 + int(max_y / 2), 45,
                f"{timer[0]} : {round(timer[1] - time.perf_counter(), 2)} : {round((timer[1] - time.perf_counter()) / 60, 2)} : {round((timer[1] - time.perf_counter()) / 3600, 2)}")
            for i, countdown in enumerate(countdown_list):
                stdscr.addstr(i + 2 + int(max_y / 2), 100,
                f"{countdown[0]} : {round(countdown[1] - time.perf_counter(), 2)} : {round((countdown[1] - time.perf_counter()) / 60, 2)} : {round((countdown[1] - time.perf_counter()) / 3600, 2)}")
        if len(stopwatch_list) > int(max_y/2) or len(timer_list) > int(max_y/2):
            stdscr.addstr(2, 45, "Please remove some stopwatches/timers/countdowns or")
            stdscr.addstr(3, 45, "increase the window size to see your current stopwatches/timers/countdowns.")
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(max_y, 45, "Press 'q' to exit." + " " * (max_x - 63))
        stdscr.attroff(curses.A_REVERSE)
        k = stdscr.getch()
    
    stdscr.timeout(-1)
    curses.echo()
    curses.curs_set(True)