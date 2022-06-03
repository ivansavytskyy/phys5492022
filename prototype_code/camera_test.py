from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
for i in range(5):
    sleep(3.0)
    try:
        camera.capture(f'/home/phys5492022/Desktop/pythonimage{i}.jpg')
    except:
        camera.stop_preview()
camera.stop_preview()