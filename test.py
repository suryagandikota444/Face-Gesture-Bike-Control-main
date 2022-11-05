import uvc
import time

def main():
    print(dir(uvc.urlparse))
    dev_list = uvc.device_list()
    cap = uvc.Capture(dev_list[0]["uid"])
    cap.frame_mode = (1280, 720, 30)
    tlast = time.time()
    for x in range(100):
        frame = cap.get_frame_robust()
        jpeg = frame.jpeg_buffer
        print("%s (%d bytes)" % (type(jpeg), len(jpeg)))
        #img = frame.img
        tnow = time.time()
        print("%.3f" % (tnow - tlast))
        tlast = tnow
    cap = None

main()