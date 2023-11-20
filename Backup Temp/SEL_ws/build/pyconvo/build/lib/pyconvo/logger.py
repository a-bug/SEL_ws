import rclpy
from rclpy.node import Node

from std_msgs.msg import UInt8MultiArray

class Logger(Node):

    def __init__(self):
        super().__init__('logger')
        self.subscription = self.create_subscription(
            UInt8MultiArray,
            'serial_read',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.log = ""

    def listener_callback(self, msg):
        for i in range(len(msg.data)):
            if msg.data[i]>31:
                self.log+=chr(msg.data[i])
            elif msg.data[i]==13:    
                self.get_logger().info('%s' % self.log)
                self.log=""

def main(args=None):
    rclpy.init(args=args)

    logger = Logger()

    rclpy.spin(logger)

    logger.destroy_node()
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()
