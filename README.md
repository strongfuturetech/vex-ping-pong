# Ping Pong

> A VEX V5 Clawbot Example demonstrating bot-to-bot communication! 🤖🛜🤖

## Setup

### Materials

You don't need a fully built bot for this one! 

At the very least you'll need:
- One V5 Robot Brain
- The battery to power that brain
- One V5 Robot Radio
- The V5 Robot Controller
- *Cables:*
    - Two smart cables (one for radio, one for controller)
    - one USB to Mini-USB controller (connect PC to brain)
    - One 4-pin connector (for the battery)

**Optional Components:**
- *Another* V5 Robot Radio for wireless control

⚠️ If you're adding a wireless controller to the mix, the bots will need their radios plugged into the highest Smart Port on the brain (21, on the side).

> "When multiple radios are connected to a V5 brain, the radio in the highest numbered smart port will be used for the controller VEXnet connection. To avoid errors, it’s recommended that the VEXnet radio be connected to port 21, any other radio will then be considered to be a VEXlink radio and configured accordingly." - [VEXlink documentation (2020)](https://www.vexforum.com/t/vexlink-documentaton/84538).

Otherwise: just plug the controller into a Smart Port.

### Configuration

Plug the radio into a free Smart Port on the brain. This project uses `Port 1`.

If you're adding a *wireless* controller to the mix, plug that one into the highest port number. If not, plug in into another port on the brain. We'll briefly use the controllers to setup the VEXLinks on the bots.

⚠️ If you use different ports for your build, update the project code to:
1. Establish the controller on the proper port.
2. Create the VEXlink on the proper port.

## Usage Info

**Controller Configuration**

- **Port:** 20

**VEXlink Configuration**

- **Port:** 1
- **Name:** 'pingpongbots'
- **Link Type:** is determined at the start of the program, using the controller.

# To Do

The Event API doesn't seem to be working as expected. (I'm thinking it's user error,) so the code works around the use of Threads. There are a few things that need to be examined.

I'm not sure how else to pause the main thread for input, so we'll see if a thread works for that.
We can also see if a thread can be used to create the VEXlinks. 

If there's a way to detect if there's already a VEXlink Manager, though, we could skip the input issue altogether. VEXbots trying to connect to the same "network" can run as a worker instead.