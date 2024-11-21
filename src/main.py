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

# Flags to keep track of certain events
GLOBAL_FLAGS = {
    "link_created": False,
    "other_bots_connected": False
}

# Function used to create VEXlinks
def establish_VEXlink():
    brain.screen.print('Link creation status: ', GLOBAL_FLAGS['link_created'])
    brain.screen.new_line()
    brain.screen.print('Press X to create a Manager Link.')
    brain.screen.new_line()
    brain.screen.print('Press B to create a Worker instead.')
    brain.screen.new_line()

    type = None
    button_not_pressed = True

    while button_not_pressed:
        if controller.buttonX.pressing():
            brain.screen.print('Creating a Manager Link...')
            brain.screen.new_line()
            type = VexlinkType.MANAGER
            button_not_pressed = False
        if controller.buttonB.pressing():
            brain.screen.print('Creating a Worker Link...')
            brain.screen.new_line()
            type = VexlinkType.WORKER
            button_not_pressed = False
    
    if type == None:
        # something happened
        brain.screen.print('Uh-oh: VEXlink type assignment failed.')
        return False

    new_link = MessageLink(Ports.PORT5, 'pingpongbots', type)
    brain.screen.print('Complete!')
    brain.screen.new_line()
    wait(3, TimeUnits.SECONDS)
    # controller.screen.clear_screen()
    brain.screen.clear_screen()
    GLOBAL_FLAGS['link_created'] = True # FIX: an event would be lovely here.
    brain.screen.print('Link creation status: ', GLOBAL_FLAGS['link_created'])
    brain.screen.new_line()
    return new_link

# ========== VEXLink messaging functions ========== #

# callback for any message received
def message_received():
    brain.screen.print("Message received!")
    brain.screen.new_line()
    msg = link.receive(500)
    brain.screen.print(msg)
    brain.screen.new_line()

    if msg == 'ping':
        on_pinged(link)
    if msg == 'pong':
        on_ponged()

# respond to ping message
def on_pinged(link):
    brain.screen.print("Pinged!")
    link.send('pong')

# respond to pong message
def on_ponged():
    brain.screen.print("Pong! Stopping here.")

# ========== VEXLink testing functions ========== #

def test_link_connection():
    # check if the link is wired up properly
    # "VEXlink radio is connected to the port specified"

    is_connected = link.installed()

    if is_connected:
        result = 'VEXLink is connected to correct port.'
    else:
        result = 'VEXLink is not connected!'

    brain.screen.print(result)
    brain.screen.new_line()

def test_link_pairing():
    # check if we're paired with the Brain
    # "A link between Manager and Workers has been established"

    is_brain_linked = link.is_linked()

    if is_brain_linked:
        result = 'Bots connected to this VEXlink can communicate.'
        GLOBAL_FLAGS['other_bots_connected'] = True
    else:
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
    brain.screen.print('Uh-oh, link creation failed somewhere.')
    brain.screen.new_line()

# Thread for continually testing VEXlink connection
def test_thread_callback():
    brain.screen.print('Hello from VEXLink Testing thread!')
    brain.screen.new_line()

    # TODO: a counter might fit in here nicely
    
    while GLOBAL_FLAGS['other_bots_connected'] == False:
        wait(7,TimeUnits.SECONDS)
        test_link_pairing()
    
    # TODO: send a signal to close the thread when other are bots detected

test_thread = Thread(test_thread_callback)

# TODO: close the testing thread on a signal.

# Start talking.
brain.screen.clear_screen()
link.received(message_received)

for i in range(3):
    brain.screen.print('Pinging...')
    link.send('ping')
    wait(4,TimeUnits.SECONDS)
    