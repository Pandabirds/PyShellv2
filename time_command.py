import curses
import threading
import time
import datetime

import superglobals
import screenfunctions

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

        if max_y >= 39 and max_x >= 159:

            if superglobals.information_enabled_setting:
                superglobals.information_enabled = True

            # Looping these variable declarations so it automatically updates on new year.
            current_year = datetime.datetime.now().year
            old_new_year = datetime.datetime(current_year, 1, 1, 0, 0, 0)
            next_new_year = datetime.datetime(current_year + 1, 1, 1, 0, 0, 0)

            stdscr.erase()
            screenfunctions.render_defaults(stdscr)
            stdscr.addstr(0, 45, str(datetime.datetime.now()))

            stdscr.addstr(2, 45, f"PyShell Running: {time.perf_counter() - superglobals.start_time}")

            stdscr.addstr(4, 45, f"Time Since New Year: {datetime.datetime.now() - old_new_year}")
            stdscr.addstr(5, 45, f"Time Until New Year: {next_new_year - datetime.datetime.now()}")

            stopwatch_list = superglobals.stopwatch_list
            timer_list = superglobals.timer_list
            countdown_list = superglobals.countdown_list
            if not (len(stopwatch_list) > int(max_y / 2) or len(timer_list) > int(max_y / 2)):
                
                for i in range(0, max_y + 1):
                    stdscr.addstr(i, 98, "│")
                    stdscr.addstr(int(max_y / 2), 45, "─" * (max_x - 45))
                
                # Displaying Stopwatches.
                for i, stopwatch in enumerate(stopwatch_list):
                    stdscr.addstr(i + 1, 100,
                    f"{stopwatch.name} : {round(time.perf_counter() - stopwatch.seconds, 2)} : {round((time.perf_counter() - stopwatch.seconds) / 60, 2)} : {round((time.perf_counter() - stopwatch.seconds) / 3600, 2)}")
                
                # Displaying Timers.
                for i, timer in enumerate(timer_list):
                    stdscr.addstr(i + 2 + int(max_y / 2), 45,
                    f"{timer.name} : {round(timer.seconds - time.perf_counter(), 2)} : {round((timer.seconds - time.perf_counter()) / 60, 2)} : {round((timer.seconds - time.perf_counter()) / 3600, 2)}")
                
                # Displaying Countdowns.
                for i, countdown in enumerate(countdown_list):
                    stdscr.addstr(i + 2 + int(max_y / 2), 100,
                    f"{countdown.name} : {round(countdown.seconds - time.perf_counter(), 2)} : {round((countdown.seconds - time.perf_counter()) / 60, 2)} : {round((countdown.seconds - time.perf_counter()) / 3600, 2)}")
                
                stdscr.addstr(int(max_y / 2), 43, "├")
                stdscr.addstr(int(max_y / 2), 98, "┼")
            if len(stopwatch_list) > int(max_y/2) or len(timer_list) > int(max_y/2):
                stdscr.addstr(2, 45, "Please remove some stopwatches/timers/countdowns or")
                stdscr.addstr(3, 45, "increase the window size to see your current stopwatches/timers/countdowns.")
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(max_y, 45, "Press 'q' to exit." + " " * (max_x - 63))
            stdscr.attroff(curses.A_REVERSE)
            k = stdscr.getch()
        
        if max_y < 39 or max_x < 159:
            superglobals.information_enabled = False
            stdscr.addstr(0, 0, "Py-Shell requires atleast a 160x40 window size.")
            stdscr.getch()                                                      
            stdscr.erase()
    
    stdscr.timeout(-1)
    curses.echo()
    curses.curs_set(True)