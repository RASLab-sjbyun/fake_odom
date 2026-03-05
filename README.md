# 1. Create Node 
```bash
cd ~/go2_sim_ws/src/fake_odom/fake_odom/
gedit odom_pub.py
cd ~/go2_sim_ws/src/fake_odom/
gedit setup.py
```
## 1.1 odom_pub.py
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

## 1.2 setup.py
  ```python
  from setuptools import find_packages, setup

  package_name = 'fake_odom'

  setup(
      name=package_name,
      version='0.0.0',
      packages=find_packages(exclude=['test']),
      data_files=[
          ('share/ament_index/resource_index/packages',
              ['resource/' + package_name]),
          ('share/' + package_name, ['package.xml']),
      ],
      install_requires=['setuptools'],
      zip_safe=True,
      maintainer='lab',
      maintainer_email='lab@todo.todo',
      description='TODO: Package description',
      license='TODO: License declaration',
      tests_require=['pytest'],
      entry_points={
          'console_scripts': [
          'odom_tf_broadcaster = fake_odom.gt_tf:main',
          'odom_local_publisher = fake_odom.odom_pub:main'
          ],
      },
  )

  ```
