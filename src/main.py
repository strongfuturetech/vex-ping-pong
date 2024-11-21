# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Strong Future Tech Training Center                           #
# 	Created:      10/31/2024, 1:24:51 PM                                       #
# 	Description:  Bot-to-bot communication example using MessageLink           #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()

# A controller is used for VEXlink setup
controller = Controller()

# Change this if you're using different ports for the VEXlink
LINK_PORT = Ports.PORT5

# Flags to keep track of certain events
GLOBAL_FLAGS = {
    "link_created": False,
    "other_bots_connected": False,
    "is_manager": False,
    "watch_screen": True,
    "screen_full": False
}

# ========== Screen Utilities ========== #

SCREEN_LINES = {
    'MAX': 12,
    'current': 0
}

def is_screen_full():
    if SCREEN_LINES['current'] >= SCREEN_LINES['MAX']:
        return True
    else:
        return False

# Clear screen and reset cursor like you'd expect from a console.
def clear_screen():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    SCREEN_LINES['current'] = 0
    GLOBAL_FLAGS['screen_full'] = False

# Colorize all brain.screen logging based on context
def log_color(context: str):
    if context == "info" or context == "i":
        if GLOBAL_FLAGS['is_manager']:
            brain.screen.set_pen_color(Color.BLUE)
        else:
            brain.screen.set_pen_color(Color.PURPLE)
    elif context == "error" or context == "e":
        brain.screen.set_pen_color(Color.RED)
    elif context == "warning" or context == "w":
        brain.screen.set_pen_color(Color.YELLOW)
    elif context == "success" or context == "s":
        brain.screen.set_pen_color(Color.GREEN)
    else:
        brain.screen.set_pen_color(Color.WHITE)

# Screen logging wrapper -- uses contextual coloring
def log_line(*args, context=''):
    log_color(context)
    brain.screen.print(*args)
    brain.screen.new_line()
    SCREEN_LINES['current'] += 1

# Screen logging wrapper that takes a Color object instead
def log_line_in_color(color: Color, *args):
    if type(color) is not Color:
        color = Color.WHITE
    
    brain.screen.set_pen_color(color)
    brain.screen.print(*args)
    brain.screen.new_line()
    SCREEN_LINES['current'] += 1

# ========== VEXLink creation function ========== #

def establish_VEXlink():
    log_line('Link creation status: ', GLOBAL_FLAGS['link_created'])
    log_line_in_color(Color.BLUE, 'Press X to create a Manager Link.')
    log_line_in_color(Color.PURPLE, 'Press B to create a Worker instead.')

    type = None
    button_not_pressed = True

    while button_not_pressed:
        if controller.buttonX.pressing():
            GLOBAL_FLAGS['is_manager'] = True
            log_line('Creating a Manager Link...', context='info')
            type = VexlinkType.MANAGER
            button_not_pressed = False
        if controller.buttonB.pressing():
            log_line('Creating a Worker Link...', context='info')
            type = VexlinkType.WORKER
            button_not_pressed = False
    
    if type == None:
        # something happened
        log_line('Uh-oh: VEXlink type assignment failed.', context='error')
        return False

    new_link = MessageLink(LINK_PORT, 'pingpongbots', type)
    log_line('Complete!', context='success')
    wait(3, TimeUnits.SECONDS)
    clear_screen()
    GLOBAL_FLAGS['link_created'] = True # FIX: an event would be lovely here.
    log_line('Link creation status: ', GLOBAL_FLAGS['link_created'])
    return new_link

# ========== VEXLink messaging functions ========== #

# callback for any message received
def message_received():
    log_line('Message received!', context='info')
    msg = link.receive(500)
    brain.screen.print(msg) # keeps returning as None... does this even go here?
    brain.screen.new_line()

    if msg == 'ping':
        on_pinged(link)
    if msg == 'pong':
        on_ponged()

# respond to ping message
def on_pinged(link: MessageLink):
    log_line('Pinged!', context='info')
    link.send('pong')

# respond to pong message
def on_ponged():
    log_line('Pong! Stopping here.')

# ========== VEXLink testing functions ========== #

def test_link_connection():
    # check if the link is wired up properly
    # "VEXlink radio is connected to the port specified"

    is_connected = link.installed()

    if is_connected:
        ctx = 'success'
        result = 'VEXLink is connected to correct port.'
    else:
        ctx = 'error'
        result = 'VEXLink is not connected!'

    log_line(result,context=ctx)

def test_link_pairing():
    # check if we're paired with the Brain
    # "A link between Manager and Workers has been established"

    is_brain_linked = link.is_linked()

    if is_brain_linked:
        ctx = 'success'
        result = 'Bots connected to this VEXlink can communicate.'
        GLOBAL_FLAGS['other_bots_connected'] = True
    else:
        ctx = 'error'
        result = 'VEXLink is not paired!'

    log_line(result,context=ctx)

# ========== Program Threads ========== #

# start watching the screen
def screen_watching_task():
    # if GLOBAL_FLAGS['watch_screen']:
    #     log_line_in_color(Color.ORANGE, 'Watching the screen!')
    
    while GLOBAL_FLAGS['watch_screen']:
        if is_screen_full():
            wait(1,TimeUnits.SECONDS)
            clear_screen()

screen_watcher = Thread(screen_watching_task)

# Create VEXLink and begin testing thread
link = establish_VEXlink()

if GLOBAL_FLAGS['link_created']:
    test_link_connection()
    test_link_pairing()
else:
    log_line('Uh-oh, link creation failed somewhere.')

# Thread for continually testing VEXlink connection
def test_thread_callback():
    log_line_in_color(Color.CYAN, 'Hello from VEXLink Testing thread!')

    # TODO: a counter might fit in here nicely
    
    while GLOBAL_FLAGS['other_bots_connected'] == False:
        wait(7,TimeUnits.SECONDS)
        test_link_pairing()
    
    # TODO: send a signal to close the thread when other are bots detected

test_thread = Thread(test_thread_callback)

# TODO: close the testing thread on a signal.

# Start talking...
# FIX: ...After 10 seconds, until we can get events in order.
# brain.screen.clear_screen()
link.received(message_received)

wait(10,TimeUnits.SECONDS)

for i in range(3):
    log_line('Pinging...', context='info')
    link.send('ping')
    wait(4,TimeUnits.SECONDS)
