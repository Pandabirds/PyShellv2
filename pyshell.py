# For the entire display system. Would use import * but that would probably break other modules.
import curses
# Variety of uses.
from platform import sys, os, uname
# Resizing Thread.
import threading
import subprocess
# Custom module for messing with the screen.
import screenfunctions # ! Create a command that pauses stopwatches/timers/countdown
# Custom module for small commands.
import smallcommands
# Custom module to use superglobal variables across modules.
import superglobals
# Calculator Command Module.
import calculator_command
# Help Command Module, holds all the built-in commands.
import help_command
# Time Command Module.
import time_command

if sys.platform.lower() != "linux" and __name__ == "__main__":
    print("This Shell is only usable on Linux")
    # Unsure what exit code to use here, I'm using 1 for now.
    sys.exit(1)


# Normally in a multi-file program I wouldn't use main(), but I want to be able to use curses.wrapper()
def main(stdscr):
    superglobals.initialize()
    curses.start_color()

    curses.use_default_colors()
    curses.init_pair(1, 225, -1)
    stdscr.attron(curses.color_pair(1))

    #curses.use_default_colors()
    #curses.init_pair(1, curses.COLOR_WHITE, -1)
    stdscr.attron(curses.A_BOLD)
    stdscr.keypad(True)

    # Displays misc information if True.
    information_enabled = True
    # I am using 2 variables, this is for when the program itself wants to change information_enabled.
    information_enabled_setting = True

    # Subtracting 1 from the values so I can do stuff at the end.
    max_y = stdscr.getmaxyx()[0] - 1
    max_x = stdscr.getmaxyx()[1] - 1


    # Using a thread for this so it auto-resizes while in a program.
    def resizing_thread_function():
        while True:
            if max_y < 39 or max_x < 159:
                # Resizes terminal automatically.
                print("\x1b[8;40;160t")

    resizing_thread = threading.Thread(target=resizing_thread_function,
    daemon=True)
    resizing_thread.start()

    timer_thread = threading.Thread(target=screenfunctions.timer_thread_function,
    daemon=True)
    timer_thread.start()

    # String for storing the last input from the user.
    input_string = ""

    # Main loop for the entire Shell.
    while True:
        max_y = stdscr.getmaxyx()[0] - 1
        max_x = stdscr.getmaxyx()[1] - 1
        stdscr.erase()
        
        if information_enabled_setting:
            superglobals.information_enabled = True

        if max_y >= 39 and max_x >= 159:

            screenfunctions.render_defaults(stdscr)

            # Getting input from user.
            input_string = screenfunctions.curses_input(stdscr, int(max_y / 2), 
            0, f"{superglobals.state}:: ", 42 - len(superglobals.state) - 3)
            # Maximum input length changes based off of state.

            cmds = input_string.split("; ")
            cmds[0] = cmds[0].lower()

            if cmds[0] == "exit" or cmds[0] == "quit":
                break
            if cmds[0] == "time" or cmds[0] == "date":
                stdscr.erase()
                screenfunctions.render_defaults(stdscr)
                superglobals.state = "time"
                time_command.main(stdscr)
                superglobals.state = "main"
            if cmds[0] == "stopwatch":
                smallcommands.stopwatch_command(cmds)
            if cmds[0] == "timer":
                smallcommands.timer_command(cmds)
            if cmds[0] == "calc" or cmds[0] == "calculator":
                stdscr.erase()
                screenfunctions.render_defaults(stdscr)
                superglobals.state = "calc"
                calculator_command.main(stdscr)
                superglobals.state = "main"
            if cmds[0] == "information" or cmds[0] == "informationtoggle":
                superglobals.information_enabled = not superglobals.information_enabled
                information_enabled_setting = False
            if cmds[0] == "help":
                stdscr.erase()
                screenfunctions.render_defaults(stdscr)
                help_command.main(stdscr, cmds)
                superglobals.state = "main"
            if cmds[0] == "countdown":
                smallcommands.bv(cmds)
        if max_y < 39 or max_x < 159:
            superglobals.information_enabled = False
            stdscr.addstr(0, 0, "Py-Shell requires atleast a 160x40 window size.")
            stdscr.getch()                                                      
    curses.endwin()

if __name__ == '__main__':
    curses.wrapper(main)