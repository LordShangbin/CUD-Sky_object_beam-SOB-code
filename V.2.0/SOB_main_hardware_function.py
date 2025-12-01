from gpiozero import OutputDevice,RotaryEncoder,Button
import time

class Encoder:
    def __init__(self, aIn,bIn,mstep):
        self.Aziencoder = RotaryEncoder(a=aIn, b=bIn, wrap=True, max_steps=mstep)
        self.last_rotary_value_Azi = 0
        self.last_rotary_value_Alt = 0 # Variable to store the last value of rotary encoder
    def Read(self):
        current_rotary_value_Azi = self.Aziencoder.steps  # Read current step count from rotary encoder
        # Check if the rotary encoder value has changed
        if self.last_rotary_value_Azi != current_rotary_value_Azi:
            return current_rotary_value_Azi  # Print the current value
        self.last_rotary_value_Azi = current_rotary_value_Azi  # Update the last value
        time.sleep(0.1)  # Short delay to prevent excessive CPU usage
    def Reset(self):
        self.Aziencoder.steps = 0
        
class stepper_motor:
    def __init__(self,en,step,dir1,En1,En2,maxstep):
        self.step_pin = OutputDevice(step)
        self.dir_pin = OutputDevice(dir1)
        self.en_pin = OutputDevice(en)
        self.encode = Encoder(En1,En2,maxstep)
        self.maxstep = maxstep
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
        self.encode.Reset()
        microstep = 16
        step_per_angle = microstep / 1.8
        total_step = int(round(step_per_angle * angle,0))
        self.drive(total_step, round(abs(total_step)/ angle_per_sec))#
        encoder_step_per_angle = self.maxstep / 360
        total_encoder_step = int(round(encoder_step_per_angle * angle))
        print(total_encoder_step , self.encode.Read())
        different = total_encoder_step - self.encode.Read()
        if different > 1:
            self.drive_angle(-different, angle_per_sec)
    def lock(self):
        self.en_pin.off()
    def unlock(self):
        self.en_pin.on()