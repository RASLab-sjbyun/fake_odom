# Create Node 
```bash
cd ~/go2_sim_ws/src/fake_odom/fake_odom/
gedit odom_pub.py
cd ~/go2_sim_ws/src/fake_odom/
gedit setup.py
```
## odom_pub.py
  ```python
  import rclpy
  from rclpy.node import Node

  from nav_msgs.msg import Odometry


  class LocalOdomPublisher(Node):

      def __init__(self):
          super().__init__('local_odom_publisher')

          self.subscription = self.create_subscription(
              Odometry,
              '/odom/ground_truth',
              self.odom_callback,
              10
          )
          self.publisher = self.create_publisher(Odometry, '/odom/local_ground_truth', 10)

          self.get_logger().info('Odom PublisherStart')

      def odom_callback(self, msg):
          odom_mgs = msg

          # TF frame
          odom_mgs.header.frame_id = 'odom'
          odom_mgs.child_frame_id = 'base_footprint'

          self.publisher.publish(odom_mgs)


  def main(args=None):
      rclpy.init(args=args)
      node = LocalOdomPublisher()
      rclpy.spin(node)
      node.destroy_node()
      rclpy.shutdown()


  if __name__ == '__main__':
      main()

  ```
