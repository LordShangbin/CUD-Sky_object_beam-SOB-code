from gpiozero import OutputDevice
import time

# Define the pins
class stepper_motor:
    def __init__(self,en,step,dir1):
        self.step_pin = OutputDevice(step)
        self.dir_pin = OutputDevice(dir1)
        self.en_pin = OutputDevice(en)
    def drive(self,steps, step_per_sec=10):
        self.dir_pin.value = steps > 0
        steps = abs(steps)
        # Loop for the given number of steps
        for _ in range(steps):
            # Set step pin high and then low
            self.step_pin.on()
            time.sleep(0.0001)
            self.step_pin.off()
            sleep_time = 1.0 / step_per_sec
            time.sleep(sleep_time)
    def drive_angle(self,angle,angle_per_sec=3):
        microstep = 16
        step_per_angle = microstep / 1.8
        print(step_per_angle)
        total_step = int(round(step_per_angle * angle,0))
        print(total_step)
        self.drive(total_step, round(abs(total_step)/ angle_per_sec))
    def lock(self):
        self.en_pin.off()
    def unlock(self):
        self.en_pin.on() 
