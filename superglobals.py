from time import perf_counter

def initialize():
    global stopwatch_list
    global timer_list
    global countdown_list
    global information_enabled
    global information_enabled_setting
    global last_calc_num
    global state
    global start_time
    global error_list

    # List that contains all the stopwatches used by the stopwatch command and the time command.
    stopwatch_list = []
    # List that contains all the timers used by the timer command and the time command.
    timer_list = []
    # List that contains all the countdowns used by the countdown command the time command.
    countdown_list = []
    # Superglobal containing whether or not the shell should display the information in the top left.
    information_enabled = True
    # Superglobal containing whether or not the User wants informaton enabled.
    information_enabled_setting = True
    # last_calc_num is a variable for keeping track of the last number used in the calculator command.
    last_calc_num = 0
    # State used for keeping track of the current program.
    state = "main"
    # Superglobal to store the amount of time PyShell has been running.
    start_time = perf_counter()
    # Superglobal that contains all passed errors.
    error_list = []