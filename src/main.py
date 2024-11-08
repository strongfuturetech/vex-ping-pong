# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Strong Future User                                           #
# 	Created:      10/31/2024, 1:24:51 PM                                       #
# 	Description:  Bot-to-bot communication example using MessageLink           #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

brain.screen.print("Hello V5")
brain.screen.new_line()

# Establish a controller - this is used for VEXlink setup
controller = Controller()

# Event callback to call to wait for input, please thanks
def wait_for_input(action):
    brain.screen.print('Waiting for input I guess?')
    wait(2,TimeUnits.SECONDS)
    action()

# Function used to create VEXlinks
def establish_VEXlink():
    brain.screen.print('Press B to create a Manager Link.')
    brain.screen.new_line()
    brain.screen.print('Press any button for a Worker instead.')
    brain.screen.new_line()

    type = None
    button_not_pressed = True

    # def est_link_type():
    #     controller.screen.print('Creating a Manager Link...')
    #     controller.screen.new_line()
    #     type = VexlinkType.MANAGER
    #     button_not_pressed = False

    def hullo():
        brain.screen.print("Hello! Input Event called.")

    # input_event = Event(wait_for_input,(est_link_type))
    input_event = Event(wait_for_input, (hullo,))
    input_event.broadcast_and_wait()

    #while button_not_pressed:
    #   controller.buttonB.pressed(est_manager)
    #   
    #   if not controller.buttonB.pressing():
    #       brain.screen.print('Creating a Worker Link...')
    #       type = VexlinkType.WORKER
    #       button_not_pressed = False
    
    # new_link = MessageLink(Ports.PORT1, 'pingpongbots', type)
    new_link = MessageLink(Ports.PORT1, 'pingpongbots', VexlinkType.MANAGER)
    controller.screen.new_line()
    controller.screen.print('Complete!')
    wait(2, TimeUnits.SECONDS)
    controller.screen.clear_screen()
    brain.screen.clear_screen()
    return new_link

# respond to ping message
def on_pinged(link):
    brain.screen.print("Pinged!")
    link.send('pong')

# respond to pong message
def on_ponged():
    brain.screen.print("Pong! Stopping here.")

## TODO: create some sorta menu that let's you set the link type
# then move all the communication code elswhere


link = establish_VEXlink()

# check if the link is connected
# "VEXlink radio is connected to the port specified"

is_connected = link.installed()

if is_connected:
    r = 'VEXLink is connected to Port 1.'
else:
    r = 'VEXLink is not connected!'

brain.screen.print(r)
brain.screen.new_line()

# check if we're paired with the Brain
# "A link between Manager and Workers has been established"

is_brain_linked = link.is_linked()

if is_brain_linked:
    r = 'Bots connected to this VEXlink can communicate.'
else:
    r = 'VEXLink is not paired!'

brain.screen.print(r)
brain.screen.new_line()

