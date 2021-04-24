import curses
import sys
import os
import threading

import screenfunctions
import superglobals

def main(stdscr):

    page = 0

    max_y = stdscr.getmaxyx()[0] - 1
    max_x = stdscr.getmaxyx()[1] - 1

    def resizing_thread_function():
        while True:
            if max_y < 39 or max_x < 159:
                print("\x1b[8;40;160t")

    def read_file(file_path, max_y, max_x):

        curses.echo(False)

        def resizing_thread_function():
            while True:
                if max_y < 39 or max_x < 159:
                    print("\x1b[8;40;160t")

        resizing_thread = threading.Thread(target=resizing_thread_function,
        daemon=True)
        resizing_thread.start()

        page = 0
        superglobals.state = "fileread"
        contents = []
        with open(file_path, "r") as file:
            contents = file.readlines()
        
        display_contents = contents
        for i in range(page * max_y, (page + 1) * max_y):
            if screenfunctions.indexists(display_contents, i):
                if len(display_contents[i]) > max_x - 44:
                    display_contents.insert(i + 1, display_contents[i][max_x - 45:])
                    display_contents[i] = display_contents[i][:max_x - 45]

        curses.curs_set(False)
        k = 0
        while k != ord('q'):
            #try:
                max_y = stdscr.getmaxyx()[0] - 1
                max_x = stdscr.getmaxyx()[1] - 1

                if max_y >= 39 and max_x >= 159:
                    if superglobals.information_enabled_setting:
                        superglobals.information_enabled = True

                    stdscr.erase()

                    screenfunctions.render_defaults(stdscr)

                    contents = []
                    with open(file_path, "r") as file:
                        contents = file.readlines()

                    display_contents = contents
                    for i, _ in enumerate(display_contents):
                        if screenfunctions.indexists(display_contents, i):
                            if len(display_contents[i]) > max_x - 44:
                                display_contents.insert(i + 1, display_contents[i][max_x - 45:])
                                display_contents[i] = display_contents[i][:max_x - 45]

                    for index, line_num in enumerate(range(page * max_y, (page + 1) * max_y)):
                        if screenfunctions.indexists(display_contents, line_num):
                            stdscr.addstr(index, 44, display_contents[line_num])

                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(max_y, 44, "Press 'q' to exit, ARROW KEYS to change pages." + " " * (max_x - 90))
                    stdscr.addstr(max_y, max_x - 9, f"Page: {page}")
                    stdscr.attroff(curses.A_REVERSE)

                    k = stdscr.getch()

                    if k == ord('q'):
                        break

                    if k == curses.KEY_RIGHT and page < 255:
                        page += 1

                    if k == curses.KEY_LEFT and page > 0:
                        page -= 1

                if max_y < 39 or max_x < 159:
                    superglobals.information_enabled = False
                    stdscr.addstr(0, 0, "Py-Shell requires atleast a 160x40 window size.")
                    stdscr.getch()                                                      
                    stdscr.erase()
        
            # except Exception as e:
            #     superglobals.error_list.append(e)

    resizing_thread = threading.Thread(target=resizing_thread_function,
    daemon=True)
    resizing_thread.start()


    while True:
        #try:
            curses.curs_set(False)
            curses.echo(False)
            
            max_y = stdscr.getmaxyx()[0] - 1
            max_x = stdscr.getmaxyx()[1] - 1

            if max_y >= 39 and max_x >= 159:

                if superglobals.information_enabled_setting:
                    superglobals.information_enabled = True

                current_directory = os.getcwd()
                current_items = os.listdir(current_directory)

                stdscr.erase()

                screenfunctions.render_defaults(stdscr)

                stdscr.addstr(1, 45, f"Current Directory :: {current_directory}")
                stdscr.addstr(1, max_x - 9, f"Page: {page}")

                # Draws the two barriers.
                screenfunctions.draw_box(stdscr, 0, 44, 2, max_x - 44, 1)
                screenfunctions.draw_box(stdscr, 3, 44, max_y - 4, max_x - 44, 1)

                # Formula for amount of files on a single page (if it is full)
                # int((max_x - 45) / 45) * (max_y - 6)
                # (int((max_x - 45) / 45) * (max_y - 6)) * page

                # Draws all the files

                # Sees if the longest filename is above 45, if it is, it sets the column modulus to that filename's length.
                column_modulus = len(max(current_items, key = len)) + 5 if len(max(current_items, key = len)) > 45 else 45
                for i in range(int((max_x - 45) / column_modulus)):
                    for ii in range(4, max_y - 1):
                        # (If you are debugging this, I apologize heavily.)
                        if screenfunctions.indexists(current_items, ((ii - 4) + (max_y - 5) * i) + (int((max_x - 45) / column_modulus) * (max_y - 6)) * page):
                            stdscr.addstr(ii, 45 + i * column_modulus, f"{(ii + (max_y - 5) * i - 4) + (int((max_x - 45) / column_modulus) * (max_y - 6)) * page} : {current_items[((ii - 4) + (max_y - 5) * i) + (int((max_x - 45) / column_modulus) * (max_y - 6)) * page]}")

                k = stdscr.getch()

                if k == ord(';'):
                    curses.echo(True)
                    #curses.cur_set(True)

                    # Gets input from the user.
                    input_string = screenfunctions.curses_input(stdscr, int(max_y / 2), 
                    0, f"{superglobals.state}:: ", 42 - len(superglobals.state) - 3)
                    
                    # Converts it into commands.
                    cmds = input_string.split("; ")
                    cmds[0] = cmds[0].lower()

                    if cmds[0] == "cd":
                        # Handling if the User inputs a path to a directory in the current directory.
                        if os.path.isdir(os.path.join(os.getcwd(), cmds[1])):
                            os.chdir(os.path.join(os.getcwd(), cmds[1]))
                        
                        # Handling if the User inputs a path to a directory not in the current directory.
                        if os.path.isdir(cmds[1]):
                            os.chdir(cmds[1])
                        
                        # Handling if the User inputs ".."
                        if cmds[1] == ".." and current_directory != "/":
                            os.chdir(os.path.dirname(current_directory))
                    
                    if cmds[0] in ["r", "read"] and screenfunctions.indexists(cmds, 1):
                        if os.path.isfile(os.path.join(os.getcwd(), cmds[1])):
                            read_file(os.path.join(os.getcwd(), cmds[1]), max_y, max_x)

                        # if os.path.isfile(cmds[1]):
                        #     read_file(cmds[1], max_y, max_x)
                        
                        superglobals.state = "multife"

                    if cmds[0] == "exit":
                        break

                    if cmds[0] == "quit":
                        sys.exit(0)

                    #curs_set(False)

                if k == curses.KEY_RIGHT and page < 255:
                    page += 1

                if k == curses.KEY_LEFT and page > 0:
                    page -= 1
            
            if max_y < 39 or max_x < 159:
                superglobals.information_enabled = False
                stdscr.addstr(0, 0, "Py-Shell requires atleast a 160x40 window size.")
                stdscr.getch()                                                      
                stdscr.erase()

        # except Exception as e:
        #     superglobals.error_list.append(e)
    curses.echo(True)
    curses.curse_set(True)