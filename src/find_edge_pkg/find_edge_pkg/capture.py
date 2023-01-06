import rclpy
from rclpy.node import Node
from test_interfaces.msg import Image
# from sensor_msgs.msg import Image
import cv2
import argparse
import time
from cv_bridge import CvBridge

def main():
    rclpy.init()
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help="type file path", required=True)
    arg = parser.parse_args()
    node = rclpy.create_node('capture')
    publisher = node.create_publisher(Image, 'capture', 10)
    cap = cv2.VideoCapture(arg.file)
    while True:
        ret, frame = cap.read()
        if ret:
            msg = Image()
            bridge = CvBridge()
            img = bridge.cv2_to_imgmsg(frame)
            msg.img = img
            publisher.publish(msg)
            time.sleep(0.1)
        else:break
    # rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    #print('start')
    pass
