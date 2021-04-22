import math
import decimal
import threading
import sys
import time
import curses

import screenfunctions
import superglobals

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
    while True:
        try:

            max_y = stdscr.getmaxyx()[0] - 1
            max_x = stdscr.getmaxyx()[1] - 1
            
            if max_y >= 39 and max_x >= 159:

                if superglobals.information_enabled_setting:
                    superglobals.information_enabled = True

                stdscr.erase()

                screenfunctions.render_defaults(stdscr)

                stdscr.addstr(1, 45, str(num))

                screenfunctions.draw_box(stdscr, 0, 44, 2, max_x - 44, 1)
                screenfunctions.draw_box(stdscr, 3, 44, 7, max_x - 44, 1)
                stdscr.addstr(4, 45, "add; [x]")
                stdscr.addstr(5, 45, "sub; [x]")
                stdscr.addstr(6, 45, "mul; [x]")
                stdscr.addstr(7, 45, "div; [x]")
                stdscr.addstr(8, 45, "pow; [x]")
                stdscr.addstr(9, 45, "root; [x]")

                stdscr.addstr(4, 59, "log")
                stdscr.addstr(5, 59, "log2")
                stdscr.addstr(6, 59, "log10")

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
                    if cmds[0] == "root" and num > 0:
                        num **= decimal.Decimal(1 / decimal.Decimal(cmds[1]))

            if max_y < 39 or max_x < 159:
                superglobals.information_enabled = False
                stdscr.addstr(0, 0, "Py-Shell requires atleast a 160x40 window size.")
                stdscr.getch()                                                      
                stdscr.erase()

        except Exception as e:
            superglobals.error_list.append(e)