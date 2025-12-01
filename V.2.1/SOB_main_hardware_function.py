from gpiozero import OutputDevice,RotaryEncoder,Button
import time

class Encoder:
    def __init__(self, aIn,bIn,mstep):
        self.encoder = RotaryEncoder(a=aIn, b=bIn, wrap=True, max_steps=mstep)
        self.last_rotary_value = 0
        self.mstep = mstep
    def Read(self): #return detected changes in angle
        encoder_value = self.encoder.steps
        angle = (encoder_value / self.mstep) * 360
        return angle 
    def Reset(self):
        self.encoder.steps = 0

class stepper_motor(Encoder):
    def __init__(self,en,step,dir1,En1,En2,maxstep):
        super().__init__(En1, En2, maxstep)
        self.step_pin = OutputDevice(step)
        self.dir_pin = OutputDevice(dir1)
        self.en_pin = OutputDevice(en)
    def drive(self, steps, step_per_sec=10):
        self.lock()
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
        self.Reset()
        microstep = 16
        step_per_angle = microstep / 1.8
        total_step = int(round(step_per_angle * angle,0))
        self.drive(total_step, round(abs(total_step)/ angle_per_sec))#
        print(angle , self.Read())
        different = angle - self.Read()
        if different > 1.04 or different < -1.04:
            self.drive_angle(-different, angle_per_sec)
    def lock(self):
        self.en_pin.off()
    def unlock(self):
        self.en_pin.on()