import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Imu, LaserScan, BatteryState
import datetime

class SensorSubscriber(Node):

    def __init__(self):
        super().__init__('sensor_subscriber')
        choices = input("What do you wanna print, choices are 1 : IMU 2 : Laser 3 : Battery 4 : Time 5 : All of the above")
        if choices == "1":
            self.imu_sub = self.create_subscription(Imu, 'imu', self.imu_callback, qos_profile=qos_profile_sensor_data)
        if choices == "2":
            self.laser_sub = self.create_subscription(LaserScan, 'scan', self.scan_callback, qos_profile=qos_profile_sensor_data)
        if choices == "3":
            self.battery_sub = self.create_subscription(BatteryState, 'battery_state', self.battery_callback, qos_profile=qos_profile_sensor_data)
        if choices == "4":
            self.timer = self.create_timer(3.0, self.timer_callback) # 1 second timer
        if choices == "5":
            self.imu_sub = self.create_subscription(Imu, 'imu', self.imu_callback, qos_profile=qos_profile_sensor_data)
            self.laser_sub = self.create_subscription(LaserScan, 'scan', self.scan_callback, qos_profile=qos_profile_sensor_data)
            self.battery_sub = self.create_subscription(BatteryState, 'battery_state', self.battery_callback, qos_profile=qos_profile_sensor_data)
            self.timer = self.create_timer(3.0, self.timer_callback) # 1 second timer
 
    def imu_callback(self, msg):
        # Print IMU data
        self.get_logger().info('IMU data: linear_accel_x = {} linear_accel_y = {} linear_accel_z = {}'.format(msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z), throttle_duration_sec=3)
        self.get_logger().info('IMU data: orientation_x = {} orientation_y = {} orientation_z = {}'.format(msg.orientation.x, msg.orientation.y, msg.orientation.z), throttle_duration_sec=3)
        self.get_logger().info('IMU data: angular_x = {} angular_y = {} angular_z = {}'.format(msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z), throttle_duration_sec=3)
      
    def scan_callback(self, msg):
        # Print Laser Scan data
        filtered_ranges = [r for r in msg.ranges if r > 0]
        self.get_logger().info('Laser Scan min data: {}'.format(min(filtered_ranges)), throttle_duration_sec=3)
        #self.get_logger().info('Laser Scan min data: {}'.format(min(msg.ranges)), throttle_duration_sec=3)
        self.get_logger().info('Laser Scan max data: {}'.format(max(msg.ranges)), throttle_duration_sec=3)
    def battery_callback(self, msg):
        # Print Battery State data
        self.get_logger().info('Battery State data: {} V'.format(msg.voltage), throttle_duration_sec=3)

    def timer_callback(self):
        # Print current time
        self.get_logger().info('Current time: {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))



def main(args=None):
    rclpy.init(args=args)
    sensor_subscriber = SensorSubscriber()
    rclpy.spin(sensor_subscriber)
    sensor_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

