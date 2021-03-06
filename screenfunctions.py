import curses
import datetime
import time
from platform import uname, sys

import superglobals

#! Deprecated 
# def tgetstr(stdscr, max_size):
#     stdscr.timeout(1)
#     out = ""
#     k = 0
#     while k != ord('\n'):
#         k = stdscr.getch()
#         if k != 0 and k != -1 and len(out) < max_size:
#             out += chr(k)
#         if k == 127:
#             stdscr.addstr(stdscr.getyx[0], len(out) - 2, ' ')
#             out = out[:len(out) - 1]
#     return out

def render_defaults(stdscr):
    """Renders the default text for the shell, used to be able to render it in all the different commands."""
    max_y = stdscr.getmaxyx()[0] - 1
    if superglobals.information_enabled:
        stdscr.addstr(0, 0, uname().system)
        stdscr.addstr(1, 0, uname().machine)
        
    for i in range(0, max_y + 1):
        stdscr.addstr(i, 43, "│")                                              # Barrier that protects program from user input.

def curses_input(window, y, x,  prompt, max_size=100):    
    """Addstr prompt, then getstr from (y, x).

    Args:
        window (window): The window to print the prompt on and get input from.
        prompt (str): The string to add to the window.

    Returns:
        str: The response from the user.
    """
    window.addstr(y, x, prompt)
    curses.echo()
    curses.curs_set(True)
    output = str(window.getstr(max_size))[2:]                                   # Using max_size to keep user from inputting past the text area wall.
    output = output[:len(output) - 1]
    #curses.curs_set(False)
    #curses.noecho()
    return output

def indexists(list, *args):                                                    # Technically doesn't have to do with the screen, but it is very useful.
    """Returns a boolean based off of whether or not all the **args as integers are a possible index in list.
    
    Args:
        list (list): The list to test.
        *args (integer): The indexes to see if they fit in list.

    Returns:
        Boolean: Whether or not all the given indexes exist in the given list.
    """    
    return all([int(arg) < len(list) for arg in args])

def timer_thread_function():
    """A function meant to be ran in a thread that checks whether or not a timer should go off now."""
    while True:
        for i, timer in enumerate(superglobals.timer_list):
            if timer.seconds - time.perf_counter() <= 0 and timer.bits & 0b01:
                superglobals.timer_list[i].bits &= 0b10
                for _ in range(10):
                    curses.beep()
                    time.sleep(0.05)
        for i, countdown in enumerate(superglobals.countdown_list):
            if countdown.seconds - time.perf_counter() <= 0 and \
            countdown.bits & 0b01:
                superglobals.countdown_list[i].bits &= 0b00
                for _ in range(10):
                    curses.beep()
                    time.sleep(0.05)

def is_int(*args):
    """Checks if the given arguments can be turned into integers."""    
    try:
        for i in args:
            int(i)
        return True
    except Exception:
        return False

def is_float(*args):
    """Checks if the given arguments can be turned into floats."""    
    try:
        for i in args:
            float(i)
        return True
    except Exception:
        return False

def draw_box(stdscr, y, x, height, width, mode=0):
    """Draws a box using box drawing characters.

    Args:
        stdscr (curses screen): The window to draw the box on.
        y (int): The y to start drawing the box at.
        x (int): The x to start drawing the box at.
        height (int): The height of the box.
        width (int): The width of the box.
        mode (int): The mode from 0-2, 0: Hard Corners, 1: Round Corners, 2: Double Hard Corners, default is 0. 
    """
    if mode == 0:
        stdscr.addstr(y, x, "┌" + "─" * (width - 1) + "┐")
        stdscr.addstr(y + height, x, "└" + "─" * (width - 1) + "┘")
        for i in range(y + 1, y + height):
            stdscr.addstr(i, x, "│")
            stdscr.addstr(i, x + width, "│")
    if mode == 1:
        stdscr.addstr(y, x, "╭" + "─" * (width - 1) + "╮")
        stdscr.addstr(y + height, x, "╰" + "─" * (width - 1) + "╯")
        for i in range(y + 1, y + height):
            stdscr.addstr(i, x, "│")
            stdscr.addstr(i, x + width, "│")
    if mode == 2:
        stdscr.addstr(y, x, "╔" + "═" * (width - 1) + "╗")
        stdscr.addstr(y + height, x, "╚" + "═" * (width - 1) + "╝")
        for i in range(y + 1, y + height):
            stdscr.addstr(i, x, "║")
            stdscr.addstr(i, x + width, "║")

# This would be very useful if completed!!!
# def wordwrap_waddstr(window, y, x, string):
#     #define function wordwrap (window, y, x, string) {
#     #   
#     #
#     #
#     #}
#     max_y = window.getmaxyx()[0] - 1
#     max_X = window.getmaxyx()[1] - 1

#     window.addstr(y, x, string[0])
#     for i in range(len(string) - 1):


#! Deprecated
# def information_show(stdscr, information_enabled):
#     """A function meant to be in a thread. It shows information in the text area.

#     Args:
#         stdscr ([type]): [description]
#         information_enabled ([type]): [description]
#     """    
#     while True:
#         if information_enabled:
#             old_position = stdscr.getyx()
#             stdscr.addstr(0, 0, sys.platform)
#             stdscr.addstr(1, 0, str(datetime.datetime.now()))
#             stdscr.refresh()
#             stdscr.move(old_position[0], old_position[1])