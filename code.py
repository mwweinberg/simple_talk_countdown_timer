import time
import board
import digitalio
import neopixel

#audio libraries
import array
import math

led = digitalio.DigitalInOut(board.D13)
led.switch_to_output()

button1 = digitalio.DigitalInOut(board.BUTTON_A)
button1.switch_to_input(pull=digitalio.Pull.DOWN)

button2 = digitalio.DigitalInOut(board.BUTTON_B)
button2.switch_to_input(pull=digitalio.Pull.DOWN)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2, auto_write=False)

number_of_pixels = 10

state = 0

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

# load audio libraries and create the sample
try:
    from audiocore import RawSample
except ImportError:
    from audioio import RawSample

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

FREQUENCY = 440  # 440 Hz middle 'A'
SAMPLERATE = 8000  # 8000 samples/second, recommended!

# Generate one period of sine wav.
length = SAMPLERATE // FREQUENCY
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / length) * (2 ** 15) + 2 ** 15)

# Enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True

audio = AudioOut(board.SPEAKER)
sine_wave_sample = RawSample(sine_wave)



# color function
def color(color):
    for i in range(number_of_pixels):
        pixels[i] = color
        pixels.show()
    print(color)


def playAudio():
    audio.play(sine_wave_sample, loop=True)  # Play the single sine_wave sample continuously...
    time.sleep(1)  # for the duration of the sleep (in seconds)
    audio.stop()  # and then stop.



def colorCountdown():
    #initial countdown
    color(GREEN)
    #time in seconds
    time.sleep(60*.1)
    color(YELLOW)
    time.sleep(30)
    #flashing stage
    cycles = 0
    while cycles < 5:
        color(YELLOW)
        time.sleep(1)
        color(OFF)
        time.sleep(1)
        cycles += 1
    color(RED)
    state = 1
    print("state = " + str(state))
    playAudio()
    return 1









while True:
    print(str(state))
    if button1.value:
        #colorSequence(state)
        if state == 0:
            state = colorCountdown()
            #color(GREEN)
            #time in seconds
            #time.sleep(5)
            #color(YELLOW)
            #time.sleep(3)
            #color(RED)
            #state = 1
            #print("state = " + str(state))
            #playAudio()
        elif state == 1:
            print("state 1")
            color(OFF)
            state = 0
            time.sleep(2)
    if button2.value:
        if state == 0:
            state = colorCountdown()
        elif state == 1:
            color(OFF)
            state = 0
            #if you dont' have some pause the button is read as both triggering OFF and restarting things
            time.sleep(2)
    else:
        pass

    time.sleep(0.05)

