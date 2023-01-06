import cv2
import numpy as np
import rclpy
from test_interfaces.msg import ColorShape
from test_interfaces.srv import ColorEvent
from cv_bridge import CvBridge

class color():
    def __init__(self, b, g, r) -> None:
        self.bridge = CvBridge()
        self.b = b
        self.g = g
        self.r = r

    def detect(self, img_ndarray):
        ori_img = self.bridge.imgmsg_to_cv2(img_ndarray, desired_encoding='passthrough')
        color_range = 60
        lowb = self.b-color_range if self.b-color_range >= 0 else 0
        lowg = self.g-color_range if self.g-color_range >= 0 else 0
        lowr = self.r-color_range if self.r-color_range >= 0 else 0
        uppb = self.b+color_range if self.b+color_range <= 255 else 255
        uppg = self.g+color_range if self.g+color_range <= 255 else 255
        uppr = self.r+color_range if self.r+color_range <= 255 else 255
        lower = np.array([lowb,lowg,lowr])
        upper = np.array([uppb,uppg,uppr])
        mask = cv2.inRange(ori_img, lower, upper)
        mask = self.bridge.cv2_to_imgmsg(mask, encoding='passthrough')
        return mask

    def change_color(self, b, g, r):
        self.b = b
        self.g = g
        self.r = r

c = False
s = color(0,0,0)

def callback(data):
    global s, c
    pub = node.create_publisher(ColorShape, 'find_color', 10)
    if not c:
        s = color(b=data.b, g=data.g, r=data.r)
        c = True
    resp = s.detect(data.a)
    msg = ColorShape()
    msg.a = resp
    msg.frame_count = data.frame_count
    pub.publish(msg)

def service_callback(data, res):
    print('receive service')
    s.change_color(b=data.b, g=data.g, r=data.r)
    res.s = 'change color ok'
    print('return')
    return res

def main():
    global node
    rclpy.init()
    node = rclpy.create_node('find_color')
    node.create_subscription(ColorShape, 'capture', callback, 10)
    node.create_service(ColorEvent, 'find_color_srv', service_callback)
    rclpy.spin(node)
    rclpy.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()