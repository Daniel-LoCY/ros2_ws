import rclpy
from rclpy.node import Node
# from std_msgs.msg import String
from test_interfaces.msg import String

class Publisher(Node):
    def __init__(self):
        super().__init__('publisher')
        self.pub = self.create_publisher(String, 'topic', 10)
        time = 0.5
        self.timer = self.create_timer(time, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello'
        self.pub.publish(msg)
        self.get_logger().info(f'Publishing {msg.data}')

def main():
    print('start')
    rclpy.init()
    pub = Publisher()
    rclpy.spin(pub)
    pub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    #print('start')
    pass
