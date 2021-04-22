import curses
import screenfunctions
import superglobals
import threading

def main(stdscr, cmds):

    curses.curs_set(False)

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

        max_y = stdscr.getmaxyx()[0] - 1
        max_x = stdscr.getmaxyx()[1] - 1

        if max_y >= 39 and max_x >= 159:

            if superglobals.information_enabled_setting:
                superglobals.information_enabled = True

            stdscr.erase()

            screenfunctions.render_defaults(stdscr)

            if k == curses.KEY_RIGHT and page < 255:
                page += 1
            if k == curses.KEY_LEFT and page > 0:
                page -= 1

            if screenfunctions.indexists(cmds, 1):
                if cmds[1] == "stopwatch":
                    if page == 0:
                        stdscr.addstr(0, 45, "Help Menu for \"stopwatch\" command")

                        stdscr.addstr(2, 45, "stopwatch : Commands for a counter that can be viewed with the \"time\" command.")
                        stdscr.addstr(3, 45, "The created stopwatch shows the amount of time since it was created.")

                        stdscr.addstr(5, 45, "List of Commands and Usages:")
                        stdscr.addstr(6, 45, "  del; [index] : Deletes the stopwatch at [index]")
                        stdscr.addstr(7, 45, "  new; [name, optional] : Creates a new stopwatch that has the name [name]. If [name] is blank,")
                        stdscr.addstr(8, 45, "  it will set it to \"stopwatch [index + 1]\"")
                        stdscr.addstr(9, 45, "  reset; [index] : Resets the stopwatch at [index]")

                if cmds[1] == "timer":
                    if page == 0:
                        stdscr.addstr(0, 45, "Help Menu for \"timer\" command")

                        stdscr.addstr(2, 45, "timer : Commands for a counter that can be viewed with the \"time\" command.")
                        stdscr.addstr(3, 45, "The created timer shows the amount of time between now and a set amount of minutes after creation.")

                        stdscr.addstr(5, 45, "List of Commands and Usages:")
                        stdscr.addstr(6, 45, "  del; [index] : Deletes the timer at [index]")
                        stdscr.addstr(7, 45, "  new; [minutes]; [name, optional] : Creates a new timer that counts to [minutes] after creation,")
                        stdscr.addstr(8, 45, "  and has the name [name]. If [name] is blank, it will set it to \"timer [index + 1]\"")
                        stdscr.addstr(9, 45, "  reset; [index] : Resets the timer at [index]")

                if cmds[1] == "countdown":
                    if page == 0:
                        stdscr.addstr(0, 45, "Help Menu for \"contdown\" command")

                        stdscr.addstr(2, 45, "countdown : Commands for a counter that counts to a hour and minute that can be viewed with the \"time\" command.")
                        stdscr.addstr(3, 45, "The created countdown counts down to a given hour and minute.")

                        stdscr.addstr(5, 45, "List of Commands and Usages:")
                        stdscr.addstr(6, 45, "  del; [index] : Deletes the countdown at [index]")
                        stdscr.addstr(7, 45, "  new; [hour]; [minute]; [name, optional] : Creates a new countdown that counts down to the")
                        stdscr.addstr(8, 45, "  [minute]th minute of [hour] has the name [name]. If [name] is blank, it will set it to \"countdown [index + 1]\"")

                if cmds[1] == "calc":
                    if page == 0:
                        stdscr.addstr(0, 45, "Help Menu for \"calc\" command")

                        stdscr.addstr(2, 45, "calc : Basic calculator for general use.")

                        
                        stdscr.addstr(5, 45, "List of Commands and Usages:")
                        stdscr.addstr(6, 45, "  [x] : Sets the current number to [x].")
                        stdscr.addstr(7, 45, "  add; [x] : Adds [x] to the current number.")
                        stdscr.addstr(8, 45, "  sub; [x] : Subtracts [x] from the current number.")
                        stdscr.addstr(9, 45, "  mul; [x] : Multiplies the current number by [x].")
                        stdscr.addstr(10, 45, "  div; [x] : Divides the current number by [x].")
                        stdscr.addstr(11, 45, "  pow; [x] : Exponentiates the current number by [x]")
                        stdscr.addstr(12, 45, "  root; [x] : Sets the current number to the [x]th root of the current number.")
                        stdscr.addstr(13, 45, "  log : Sets the current number to the natural log of the current number.")
                        stdscr.addstr(14, 45, "  log2 : Sets the current number to the log2 of the current number.")
                        stdscr.addstr(15, 45, "  log10 : Sets the current number to the log10 of the current number.")

                if cmds[1] == "time":
                    if page == 0:
                        stdscr.addstr(0, 45, "Help Menu for \"time\" command")

                        stdscr.addstr(2, 45, "time : A menu displaying a variety of information about the time.")

                        stdscr.attron(curses.A_BOLD)
                        stdscr.addstr(5, 45, "Time does not have any commands")
                        stdscr.attroff(curses.A_BOLD)
                        
                        stdscr.addstr(7, 45, "The \"time\" menu has 4 panels.")
                        
                        stdscr.addstr(9, 45, "The first panel displays general information, such as the current date.")

                        stdscr.addstr(11, 45, "The second panel displays current stopwatches.")

                        stdscr.addstr(11, 45, "The third panel displays current timers.")
                        
                        stdscr.addstr(13, 45, "The fourth and final panel displays current countdowns.")

            if not screenfunctions.indexists(cmds, 1):
                if page == 0:
                    stdscr.addstr(0, 45, "Welcome to the Help Menu")
                    stdscr.addstr(1, 45, "You can type \"help; [command]\" to find sub-commands for a command.")
                    stdscr.addstr(2, 45, "If nothing appears, it means there are no sub-commands for that command.")

                    stdscr.addstr(4, 45, "Basic Syntax: The basic syntax cmd; option1; option2")

                    stdscr.addstr(6, 45, "List of Commands and Usages:")
                    #a
                    #b
                    #c
                    stdscr.addstr(7, 45, "  calc : Starts the calculator.")
                    stdscr.addstr(8, 45, "  color; [col] : Changes the text color (0-255).")
                    stdscr.addstr(9, 45, "  countdown; [cmd]; {options} : Uses the countdown command, see \"help; countdown\" for more details.")
                    #d
                    #e
                    #f
                    #g
                    #h
                    stdscr.addstr(10, 45, "  help; [cmd] : Shows help about [cmd], if no [cmd] is entered, it shows this screen.")
                    #i
                    stdscr.addstr(11, 45, "  information : Toggles the top left information.")
                    #j
                    #k
                    #l
                    #m
                    #n
                    #o
                    #p
                    #q
                    stdscr.addstr(12, 45, "  quit : Quits PyShell.")
                    #r
                    #s
                    stdscr.addstr(13, 45, "  stopwatch; [cmd]; {options} : Uses the stopwatch command, see \"help; stopwatch\" for more details.")
                    #t
                    stdscr.addstr(9, 45, "  time : Opens the time menu.")
                    stdscr.addstr(9, 45, "  timer; [cmd]; {options} : Uses the timer command, see \"help; timer\" for more details.")
                    #u
                    #v
                    #w
                    #x
                    #y
                    #z
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(max_y, 45, "Press 'q' to exit, ARROW KEYS to change pages." + " " * (max_x - 91))
            stdscr.addstr(max_y, max_x - 9, f"Page: {page}")
            stdscr.attroff(curses.A_REVERSE)

            k = stdscr.getch()
        
        if max_y < 39 or max_x < 159:
            superglobals.information_enabled = False
            stdscr.addstr(0, 0, "Py-Shell requires atleast a 160x40 window size.")
            stdscr.getch()                                                      
            stdscr.erase()
    
    curses.echo()
    curses.curs_set(True)