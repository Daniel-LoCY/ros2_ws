#!/usr/bin/env python3
import rclpy
from test_interfaces.srv import Edge
import cv2
from cv_bridge import CvBridge
import sys

def main():
    if len(sys.argv) == 2:
        arg = sys.argv[1]
    else:
        sys.exit('Please type number')

    rclpy.init()
    node = rclpy.create_node('event')
    client = node.create_client(Edge, 'edge_service')
    while not client.wait_for_service(1.0):
        node.get_logger().info('no response')
    req = Edge.Request()
    req.num = int(arg)
    future = client.call_async(req)
    rclpy.spin_until_future_complete(node=node, future=future)
    node.get_logger().info(future.result().str)
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()