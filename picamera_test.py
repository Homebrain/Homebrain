import picamera
import sys
from time import sleep
from datetime import datetime
import argparse

camera = picamera.PiCamera()

parser = argparse.ArgumentParser(
         prog='PROG',
         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--timer', action="store_true", help='Start with this argument to take a picture every N seconds and save it')
parser.add_argument('--timer-interval', default=60, type=int,
        help='Start with this argument to take a picture every N seconds and save it')

args = parser.parse_args()
print(args)

def menu():
    while True:
        choice = int(input("(1) Image\n(2) Video\n(0) Exit\n> "))
        if choice == 1:
            filename = "image.jpg"
            camera.capture(filename)
            print("Saved image to: {}".format(filename))
        elif choice == 2:
            filename = "video.h264"
            record_time = 10
            print("Recording {} seconds of video...".format(record_time))
            camera.start_recording(filename)
            sleep(record_time)
            camera.stop_recording()
            print("Done! Saved video to: {}".format(filename))
        elif choice == 0:
            break
        else:
            print("Invalid choice")

if args.timer:
    while True:
        now = datetime.today()
        filename = "images/{}.jpg".format(now.isoformat().split(".")[0].replace(":", "-"))
        camera.capture(filename)
        print(filename)
        sleep(args.timer_interval)
else:
    menu()

