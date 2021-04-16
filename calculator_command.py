import curses
import math
import decimal
import screenfunctions
import superglobals
import threading
import sys
import time

def main(stdscr):

    max_y = stdscr.getmaxyx()[0] - 1
    max_x = stdscr.getmaxyx()[1] - 1

    def resizing_thread_function():
        while True:
            if max_y < 39 or max_x < 159:
                print("\x1b[8;40;160t")



    resizing_thread = threading.Thread(target=resizing_thread_function,
    daemon=True)
    resizing_thread.start()

    num = decimal.Decimal(superglobals.last_calc_num)

    input_string = ""
    try:
        while True:
            stdscr.erase()

            screenfunctions.render_defaults(stdscr)

            stdscr.addstr(1, 45, str(num))

            stdscr.addstr(3, 45, "add; [x]")
            stdscr.addstr(stdscr.getyx()[0] + 1, 45, "sub; [x]")
            stdscr.addstr(stdscr.getyx()[0] + 1, 45, "mul; [x]")
            stdscr.addstr(stdscr.getyx()[0] + 1, 45, "div; [x]")
            stdscr.addstr(stdscr.getyx()[0] + 1, 45, "pow; [x]")
            stdscr.addstr(stdscr.getyx()[0] + 1, 45, "root; [x]")

            stdscr.addstr(3, 60, "log")
            stdscr.addstr(stdscr.getyx()[0] + 1, 59, "log2")
            stdscr.addstr(stdscr.getyx()[0] + 1, 59, "log10")

            input_string = screenfunctions.curses_input(stdscr, int(max_y / 2),
            0, f"{superglobals.state}:: ", 42 - len(superglobals.state) - 3)

            cmds = input_string.split("; ")
            cmds[0] = cmds[0].lower()

            for i, cmd in enumerate(cmds):
                if i != 0:
                    if cmds[i] == "pi":
                        cmds[i] = "3.141592653"
                    if cmds[i] == "tau":
                        cmds[i] = "6.283185307"
                    if cmds[i] == "phi":
                        cmds[i] = "1.618033988"
                    if cmds[i] == "e":
                        cmds[i] = "2.718281828"

            if cmds[0] == "exit":
                superglobals.last_calc_num = num
                return
            if cmds[0] == "quit":
                sys.exit(0)
            if screenfunctions.is_float(cmds[0]):
                num = decimal.Decimal(cmds[0])
            if cmds[0] == "log" and num > 0:
                num = decimal.Decimal(math.log(num))
            if cmds[0] == "log2" and num > 0:
                num = decimal.Decimal(math.log2(num))
            if cmds[0] == "log10" and num > 0:
                num = decimal.Decimal(math.log10(num))
            if screenfunctions.indexists(cmds, 1):
                if cmds[0] == "add":
                    num += decimal.Decimal(cmds[1])
                if cmds[0] == "sub":
                    num -= decimal.Decimal(cmds[1])
                if cmds[0] == "mul":
                    num *= decimal.Decimal(cmds[1])
                if cmds[0] == "div" and cmds[1] != "0":
                    num /= decimal.Decimal(cmds[1])
                if cmds[0] == "pow":
                    num **= decimal.Decimal(cmds[1])
                if cmds[0] == "root":
                    num **= decimal.Decimal(1 / decimal.Decimal(cmds[1]))
    except Exception as e:
        pass