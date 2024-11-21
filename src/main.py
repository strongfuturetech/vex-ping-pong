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
brain=Brain()

# Establish a controller - this is used for VEXlink setup
controller = Controller()

# ========== Utilities ========== #

# Change this if you're using different ports for the VEXlink
LINK_PORT = Ports.PORT5

# Flags to keep track of certain events
GLOBAL_FLAGS = {
    "link_created": False,
    "other_bots_connected": False,
    "is_manager": False
}

# Shorthand to colorize all brain.screen logging for readability.
def log_color(context):
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

# Function used to create VEXlinks
def establish_VEXlink():
    brain.screen.print('Link creation status: ', GLOBAL_FLAGS['link_created'])
    brain.screen.new_line()
    brain.screen.set_pen_color(Color.BLUE)
    brain.screen.print('Press X to create a Manager Link.')
    brain.screen.new_line()
    brain.screen.set_pen_color(Color.PURPLE)
    brain.screen.print('Press B to create a Worker instead.')
    brain.screen.new_line()

    type = None
    button_not_pressed = True

    while button_not_pressed:
        if controller.buttonX.pressing():
            log_color('mgr')
            brain.screen.print('Creating a Manager Link...')
            brain.screen.new_line()
            type = VexlinkType.MANAGER
            GLOBAL_FLAGS['is_manager'] = True
            button_not_pressed = False
        if controller.buttonB.pressing():
            log_color('worker')
            brain.screen.print('Creating a Worker Link...')
            brain.screen.new_line()
            type = VexlinkType.WORKER
            button_not_pressed = False
    
    if type == None:
        # something happened
        log_color('error')
        brain.screen.print('Uh-oh: VEXlink type assignment failed.')
        return False

    new_link = MessageLink(LINK_PORT, 'pingpongbots', type)
    log_color('success')
    brain.screen.print('Complete!')
    brain.screen.new_line()
    wait(3, TimeUnits.SECONDS)
    # controller.screen.clear_screen()
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    GLOBAL_FLAGS['link_created'] = True # FIX: an event would be lovely here.
    log_color('')
    brain.screen.print('Link creation status: ', GLOBAL_FLAGS['link_created'])
    brain.screen.new_line()
    return new_link

# ========== VEXLink messaging functions ========== #

# callback for any message received
def message_received():
    log_color('info')
    brain.screen.print("Message received!")
    brain.screen.new_line()
    msg = link.receive(500)
    brain.screen.print(msg) # keeps returning as None... does this even go here?
    brain.screen.new_line()

    if msg == 'ping':
        on_pinged(link)
    if msg == 'pong':
        on_ponged()

# respond to ping message
def on_pinged(link):
    log_color('info')
    brain.screen.print("Pinged!")
    brain.screen.new_line()
    link.send('pong')

# respond to pong message
def on_ponged():
    log_color('info')
    brain.screen.print("Pong! Stopping here.")
    brain.screen.new_line()

# ========== VEXLink testing functions ========== #

def test_link_connection():
    # check if the link is wired up properly
    # "VEXlink radio is connected to the port specified"

    is_connected = link.installed()

    if is_connected:
        log_color('success')
        result = 'VEXLink is connected to correct port.'
    else:
        log_color('error')
        result = 'VEXLink is not connected!'

    brain.screen.print(result)
    brain.screen.new_line()

def test_link_pairing():
    # check if we're paired with the Brain
    # "A link between Manager and Workers has been established"

    is_brain_linked = link.is_linked()

    if is_brain_linked:
        log_color('success')
        result = 'Bots connected to this VEXlink can communicate.'
        GLOBAL_FLAGS['other_bots_connected'] = True
    else:
        log_color('error')
        result = 'VEXLink is not paired!'

    brain.screen.print(result)
    brain.screen.new_line()

# ========== Program Threads ========== #

# Create VEXLink and begin testing thread

link = establish_VEXlink()

if GLOBAL_FLAGS['link_created']:
    test_link_connection()
    test_link_pairing()
else:
    log_color('')
    brain.screen.print('Uh-oh, link creation failed somewhere.')
    brain.screen.new_line()

# Thread for continually testing VEXlink connection
def test_thread_callback():
    brain.screen.set_pen_color(Color.CYAN)
    brain.screen.print('Hello from VEXLink Testing thread!')
    brain.screen.new_line()

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
    log_color('info')
    brain.screen.print('Pinging...')
    brain.screen.new_line()
    link.send('ping')
    wait(4,TimeUnits.SECONDS)
    