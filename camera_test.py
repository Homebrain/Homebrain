import picamera
from time import sleep

camera = picamera.PiCamera()

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
