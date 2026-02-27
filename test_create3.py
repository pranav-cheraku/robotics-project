from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Create3

robot = Create3(Bluetooth())

@event(robot.when_play)
async def play(robot):
    print("Connected to the robot...")
    await robot.set_lights_rgb(0, 255, 0)
    
    for i in range(4):
        await robot.move(10)
        await robot.turn_left(90)
    
    await robot.set_lights_rgb(255, 255, 255)

robot.play()