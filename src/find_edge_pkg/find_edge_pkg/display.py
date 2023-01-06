import rclpy
from rclpy.node import Node
from test_interfaces.msg import Image
import cv2
from cv_bridge import CvBridge

def find_edge_callback(data):
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(data.img, desired_encoding='passthrough')
    print(img.shape)
    img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
    cv2.imshow('1', img)
    cv2.waitKey(1)

def main():
    global node
    print('start display')
    rclpy.init()
    node = rclpy.create_node('display')
    node.create_subscription(Image, 'find_edge', find_edge_callback, 10)
    rclpy.spin(node)
    rclpy.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    pass