import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import String

class TurtlebotImagePublisher(Node):

    def __init__(self):
        super().__init__('turtlebot_image_publisher')
        self.publisher_ = self.create_publisher(Image, 'camera/image_raw', 10)
        #self.hello_pub_ = self.create_publisher(String, 'hello_world', 10)
        self.bridge = CvBridge()
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.capture.set(cv2.CAP_PROP_FPS, 30)

    def publish_image(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.resize(frame,(320,240))
            image_msg = self.bridge.cv2_to_imgmsg(frame, "bgr8")
            image_msg.header.stamp = self.get_clock().now().to_msg()
            self.publisher_.publish(image_msg)
            #hello_msg = String()
            #hello_msg.data = "Hello World!"
            #self.hello_pub_.publish(hello_msg)
            #print("MESSAGE PUBLISHED")

def main(args=None):
    
    rclpy.init(args=args)

    turtlebot_image_publisher = TurtlebotImagePublisher()
  
    timer_period = 0.033  # 30 FPS
    timer = turtlebot_image_publisher.create_timer(timer_period, turtlebot_image_publisher.publish_image)

    rclpy.spin(turtlebot_image_publisher)

    turtlebot_image_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
