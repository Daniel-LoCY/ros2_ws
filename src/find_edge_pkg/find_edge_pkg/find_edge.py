import rclpy
from rclpy.node import Node
from test_interfaces.msg import String, Image
from test_interfaces.srv import Edge
# from sensor_msgs.msg import Image
import cv2
import argparse
from cv_bridge import CvBridge

x = 150

def capture_callback(data):
    publisher = node.create_publisher(Image, 'find_edge', 10)
    global x
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(data.img, desired_encoding='passthrough')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blurred, 30, x)
    output = bridge.cv2_to_imgmsg(canny, encoding='passthrough')
    msg = Image()
    msg.img = output
    publisher.publish(msg)

def srv_callback(req, res):
    global x
    x = req.num
    res.str = 'ok'
    return res

def main():
    global node
    print('start find edge')
    rclpy.init()
    node = rclpy.create_node('find_edge')
    subscriber = node.create_subscription(Image, 'capture', capture_callback, 10)
    node.create_service(Edge, 'edge_service', srv_callback)
    rclpy.spin(node)
    rclpy.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    pass