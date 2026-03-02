from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Create3

# Bluetooth connection to the robot using its name
robot = Create3(Bluetooth('bard'))

@event(robot.when_play)
async def play(robot):
    print("Connected to the robot...")
    await robot.set_lights_rgb(0, 255, 0)   # Set lights to green
    await robot.play_note(440, 0.25)    # Play a note for 0.25 seconds
    
    battery_level = await robot.get_battery_level() # Get the battery level
    print(f"Battery level: {battery_level}%")

    # for i in range(5):
    #     await robot.move(186)
    #     await robot.turn_left(180)
    
    # await robot.set_lights_rgb(255, 255, 255) # Set lights to white

robot.play()