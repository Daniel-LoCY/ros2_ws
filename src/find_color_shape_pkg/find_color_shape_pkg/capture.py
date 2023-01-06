import rclpy
from test_interfaces.msg import ColorShape
import sys
import cv2
from cv_bridge import CvBridge
import time
import argparse

def talker(img_path, shape, color, frame_count):
    pub = node.create_publisher(ColorShape, 'capture', 10)
    bridge = CvBridge()
    img = bridge.cv2_to_imgmsg(img_path, encoding='passthrough')
    msg = ColorShape()
    msg.a = img
    msg.frame_count = frame_count
    c = color.replace(' ', '').split(',')
    l = []
    try:
        for i in range(len(c)):
            l.append(int(c[i]))
    except:
        exit('--color argument type failed')
    msg.b = l[0]
    msg.g = l[1]
    msg.r = l[2]
    msg.shape = int(shape)
    pub.publish(msg)
    
def video(file, shape=None, color=None):
    cap = cv2.VideoCapture(file)
    if not cap.isOpened():
        print('Cannot open camera')
        sys.exit()
    else:
        count = 1
        total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        while True:
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)))
                talker(frame, shape, color, count)
                # cv2.imshow('original', frame)
                # cv2.waitKey(10)
                time.sleep(1/100)
                print(f' 播放進度： {count}/{total_frame}', end = '\r')
                count = count + 1
            else:break

def main():
    global node
    rclpy.init()
    node = rclpy.create_node('capture')
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='type image or video path', required=True)
    parser.add_argument('--shape', default=3, help="type shape")
    parser.add_argument('--color', default='255,255,255', help="type color's BGR ex: --color 0,0,255")
    arg = parser.parse_args()
    file, shape, color = arg.file, arg.shape, arg.color
    video(file=file, shape=shape, color=color)

if __name__ == '__main__':
    main()