import curses
import screenfunctions
import superglobals
import threading

def main(stdscr, cmds):

    page = 0

    cmds = [cmd.lower() for cmd in cmds]

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

        stdscr.erase()

        max_y = stdscr.getmaxyx()[0] - 1
        max_x = stdscr.getmaxyx()[1] - 1

        screenfunctions.render_defaults(stdscr)

        if page == 0:
            stdscr.addstr(0, 45, "Welcome to the Help Menu")
            stdscr.addstr(1, 45, "You can type \"help; [command]\" to find sub-commands for a command.")
            stdscr.addstr(2, 45, "If nothing appears, it means there are no sub-commands for that command.")

            stdscr.addstr(4, 45, "Basic Syntax: The basic syntax for ")

        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(max_y, 45, "Press 'q' to exit." + " " * (max_x - 63))
        stdscr.attroff(curses.A_REVERSE)

        k = stdscr.getch()
    
    curses.echo()
    curses.curs_set(True)