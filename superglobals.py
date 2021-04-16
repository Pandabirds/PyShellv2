#TODO: Figure out how this works... I have no clue.
def initialize():
    global stopwatch_list
    global timer_list
    global countdown_list
    global information_enabled
    global last_calc_num
    global state

    # List that contains all the stopwatches used by the stopwatch command and the time command.
    stopwatch_list = []
    # List that contains all the timers used by the timer command and the time command.
    timer_list = []
    # List that contains all the countdowns used by the countdown command the time command.
    countdown_list = []
    # Superglobal containing whether or not the shell should display the information in the top left.
    information_enabled = True
    # last_calc_num is a variable for keeping track of the last number used in the calculator command.
    last_calc_num = 0
    # State used for keeping track of the current program.
    state = "main"