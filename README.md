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

# 2. PointCloude to LaserScan
## 2.1 Package Install 
  ```bash
  sudo apt install ros-humble-velodyne-laserscan
  ```
## 2.2 excute Package 
  ```bash
  ros2 run velodyne_laserscan velodyne_laserscan_node  --ros-args  -r cloud:=/velodyne_points -r scan:=/scan
  ```

# 3. Navigation Package Install
## 3.1 Package Install 
  ```bash
  sudo apt install ros-humble-bondcpp
  sudo apt install libsuitesparse-dev
  sudo apt install ros-humble-navigation2
  sudo apt install ros-humble-nav2-bringup
  ```

# 4. SLAM Package Install
## 4.1 Package Install 
  ```bash
  cd ~/go2_sim_ws/src/
  git clone -b humble https://github.com/SteveMacenski/slam_toolbox.git
  cd ~/go2_sim_ws
  colcon build
  ```

# 5. Gazebo SLAM
## Terminal 1 
  ```bash
  cd ~/go2_sim_ws/
  source install/setup.bash
  ros2 launch go2_config gazebo_velodyne.launch.py rviz:=true
  ```
## Terminal 2 
  ```bash
  cd ~/go2_sim_ws/
  source install/setup.bash
  ros2 run fake_odom odom_tf_broadcaster
  ```
## Terminal 3
  ```bash
  cd ~/go2_sim_ws/
  source install/setup.bash
  ros2 run fake_odom odom_local_publisher
  ```
## Terminal 4
  ```bash
  ros2 run velodyne_laserscan velodyne_laserscan_node  --ros-args   -r cloud:=/velodyne_points -r scan:=/scan
  ```
## Terminal 5
  ```bash
  cd ~/go2_sim_ws/
  source install/setup.bash
  ros2 launch slam_toolbox online_async_launch.py
  ```
## Terminal 6
  ```bash
  ros2 run teleop_twist_keyboard teleop_twist_keyboard
  ```
## Terminal 7
  ```bash
  ros2 run nav2_map_server map_saver_cli -f ~/map
  ```

# 6. Gazebo Navigation
## Terminal 1 
  ```bash
  cd ~/go2_sim_ws/
  source install/setup.bash
  ros2 launch go2_config gazebo_velodyne.launch.py rviz:=true
  ```
## Terminal 2 
  ```bash
  cd ~/go2_sim_ws/
  source install/setup.bash
  ros2 run fake_odom odom_tf_broadcaster
  ```
## Terminal 3
  ```bash
  cd ~/go2_sim_ws/
  source install/setup.bash
  ros2 run fake_odom odom_local_publisher
  ```
## Terminal 4
  ```bash
  ros2 run velodyne_laserscan velodyne_laserscan_node  --ros-args   -r cloud:=/velodyne_points -r scan:=/scan
  ```
## Terminal 5
  ```bash
  ros2 run teleop_twist_keyboard teleop_twist_keyboard
  ```
## Terminal 6
  ```bash
  ros2 launch nav2_bringup bringup_launch.py use_sim_time:=true map:=/home/lab/map.yaml
  ```
