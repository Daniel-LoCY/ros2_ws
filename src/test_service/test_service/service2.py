from example_interfaces.srv import AddTwoInts

import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service2')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints2', self.add_two_ints_callback)
        self.clinet = self.create_client(AddTwoInts, 'add_two_ints')

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))
        while not self.clinet.wait_for_service(1.0):
            self.get_logger().info('no resonse')
        req = AddTwoInts.Request()
        req.a = response.sum
        req.b = 3
        self.future = self.clinet.call_async(req)
        rclpy.spin_until_future_complete(self, self.future)
        self.get_logger().info('response 1')
        response.sum = self.future.result().sum
        return response


def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()