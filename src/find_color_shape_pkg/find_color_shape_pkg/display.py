import rclpy
from test_interfaces.msg import ColorShape
from test_interfaces.srv import Event, ColorEvent, ShapeEvent
import cv2
from cv_bridge import CvBridge
import numpy as np
import time
import threading


class show():
    def __init__(self) -> None:
        self.bridge = CvBridge()
        self.mask_dict = {}
        self.shape_dict = {}
        self.frame_dict = {}
        self.count = 1
        self.start = False

    def show_image(self):
        while True:
            try:
                bridge = CvBridge()
                output = bridge.imgmsg_to_cv2(self.frame_dict[str(self.count)], desired_encoding='passthrough')
                if type(self.mask_dict[str(self.count)]) == np.ndarray:
                    output = cv2.bitwise_and(output, output, mask = self.mask_dict[str(self.count)]) 
                shapex, shapey, shape, user_shape = self.shape_dict[str(self.count)]
                for i in range(len(shapex)):
                    if shape == user_shape:
                        if shape == 3:
                            cv2.putText(output, 'triangle', (shapex[i]-10, shapey[i]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        elif shape == 4:
                            cv2.putText(output, 'rectangle', (shapex[i]-10, shapey[i]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    else:
                        if user_shape == 0 and shape > 4:
                            cv2.putText(output, 'circle', (shapex[i]-10, shapey[i]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                self.shape_dict.pop(str(self.count))        
                self.mask_dict.pop(str(self.count))        
                self.frame_dict.pop(str(self.count))      
                self.count = self.count + 1
                cv2.imshow('result', output)
                cv2.waitKey(1)
            except Exception as e:
                self.count = self.count + 1
                time.sleep(0.1)

    def change_frame(self, imgmsg, frame_count):
        self.frame_dict[str(frame_count)] = imgmsg

    def change_mask(self, mask, frame_count):
        mask = self.bridge.imgmsg_to_cv2(mask, desired_encoding='passthrough')
        self.mask_dict[str(frame_count)] = mask

    def change_shape(self, x, y, shape, frame_count, user_shape):
        self.shape_dict[str(frame_count)] = [x, y, shape, user_shape]

def color_callback(data):
    s.change_mask(data.a, data.frame_count)

def callback(data):
    s.change_frame(data.a, data.frame_count)

def shape_callback(data):
    s.change_shape(data.shapex, data.shapey, data.shape, data.frame_count, data.user_shape)
    if not s.start:
        s.count = data.frame_count
        t.start()
        s.start = True

def event_callback(data, res):
    global node
    # print(data)

    # client = node.create_client(ShapeEvent, 'find_shape_srv')
    # while not client.wait_for_service(1.0):
    #     node.get_logger().info('no response')
    # req = ShapeEvent.Request()
    # req.shape = data.shape
    # future = client.call_async(req)
    # rclpy.spin_until_future_complete(node=node, future=future)
    # node.get_logger().info(future.result().s)

    client2 = node.create_client(ColorEvent, 'find_color_srv')
    while not client2.wait_for_service(1.0):
        node.get_logger().info('no response')
    node.get_logger().info('callback')
    req = ColorEvent.Request()
    req.b = data.b
    req.g = data.g
    req.r = data.r
    future = client2.call_async(req)
    node.get_logger().info('call C done..')
    # rclpy.spin_once(node)
    # rclpy.spin_once(node)
    # rclpy.spin_once(node)
    # rclpy.spin_once(node)
    # rclpy.spin_once(node)
    node.get_logger().info('spin done')
    rclpy.spin_until_future_complete(node=node, future=future)
    while future.done() is False:
        rclpy.spin_once(node)
        node.get_logger().info('not yet')
    # node.get_logger().info(future.result().s)
    res.s = 'change ok'
    node.get_logger().info('return')
    return res

def main():
    global s, t, node
    rclpy.init()
    node = rclpy.create_node('display')
    node.create_subscription(ColorShape, 'find_shape', shape_callback, 10)
    node.create_subscription(ColorShape, 'find_color', color_callback, 10)
    node.create_subscription(ColorShape, 'capture', callback, 10)
    node.create_service(Event, 'display', event_callback)
    s = show()
    t = threading.Thread(target=s.show_image)
    t.daemon = True


    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()