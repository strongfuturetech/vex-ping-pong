# Ping Pong

> A VEX V5 Clawbot Example demonstrating bot-to-bot communication! 🤖🛜🤖

## Setup

### Materials

You don't need a fully built bot for this one! 

At the very least you'll need:
- One V5 Robot Brain
    - *Two* would be ideal, of course.
- The battery to power that brain
- One V5 Robot Radio
- The V5 Robot Controller
- *Cables:*
    - Two smart cables (one for radio, one for controller)
    - one USB to Mini-USB controller (connect PC to brain)
    - One 4-pin connector (for the battery)

**Optional Components:**
- *Another* V5 Robot Radio for wireless control
- Alternatively: *another* smart cable to directly link the brains together.

⚠️ If you're adding a wireless controller to the mix, the bots will need their radios plugged into the highest Smart Port on the brain (21, on the side).

> "When multiple radios are connected to a V5 brain, the radio in the highest numbered smart port will be used for the controller VEXnet connection. To avoid errors, it’s recommended that the VEXnet radio be connected to port 21, any other radio will then be considered to be a VEXlink radio and configured accordingly." - [VEXlink documentation (2020)](https://www.vexforum.com/t/vexlink-documentaton/84538).

Otherwise: just plug the controller into a Smart Port **or** use another smart cable to establish a wired connection between both brains.
- ⚠️ Wired VEXlink connectivity hasn't been tested, yet.

### Configuration

Plug the radio into a free Smart Port on the brain. This project uses `Port 5`.

If you're adding a *wireless* controller to the mix, plug that one into the highest port number. If not, plug in into another port on the brain. We'll briefly use the controllers to setup the VEXLinks on the bots.

⚠️ If you use different radio/cable ports for your build, update the constant `LINK_PORT` to create the VEXlink on the proper one.

## Usage Info

**Controller Configuration**

- **Port options:** 
    - 10 if plugging directly into brain
    - 21 if using a second radio

**VEXlink Configuration**

- **(Default) Port:** 5
- **Name:** `pingpongbots`
- **Link Type:** is determined at the start of the program, using the controller.
