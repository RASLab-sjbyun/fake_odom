import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

from tf_transformations import euler_from_quaternion, quaternion_from_euler


class OdomTFBroadcaster(Node):

    def __init__(self):
        super().__init__('odom_tf_broadcaster')

        self.tf_broadcaster = TransformBroadcaster(self)

        self.subscription = self.create_subscription(
            Odometry,
            '/odom/ground_truth',
            self.odom_callback,
            10
        )

        self.get_logger().info('Odom TF Broadcaster started')

    def odom_callback(self, msg: Odometry):
        t = TransformStamped()

        # ⏱ timestamp: odometry 기준
        t.header.stamp = msg.header.stamp

        # TF frame
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'

        # 위치 (2D)
        t.transform.translation.x = msg.pose.pose.position.x
        t.transform.translation.y = msg.pose.pose.position.y
        t.transform.translation.z = 0.0

        # orientation → yaw만 사용
        q = msg.pose.pose.orientation
        _, _, yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])

        q_tf = quaternion_from_euler(0.0, 0.0, yaw)
        t.transform.rotation.x = q_tf[0]
        t.transform.rotation.y = q_tf[1]
        t.transform.rotation.z = q_tf[2]
        t.transform.rotation.w = q_tf[3]

        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = OdomTFBroadcaster()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

