"""Lab 4: Follow the Gap (Python skeleton).

Edit this file. Complete every `TODO`. See README.md for the algorithm
and grading rubric. Do NOT change the class name (`ReactiveFollowGap`) —
the autograder imports it by that name.
"""
import math

import rclpy
from rclpy.node import Node

import numpy as np
from sensor_msgs.msg import LaserScan
from ackermann_msgs.msg import AckermannDriveStamped


class ReactiveFollowGap(Node):
    """Reactive obstacle-avoidance: find the largest free-space gap in the
    LiDAR scan and steer toward a point inside it."""

    def __init__(self):
        super().__init__('reactive_node')

        lidarscan_topic = '/scan'
        drive_topic = '/drive'

        # TODO: subscribe to LaserScan on `lidarscan_topic` → self.lidar_callback
        # TODO: publish AckermannDriveStamped on `drive_topic`
        # self.scan_sub = self.create_subscription(...)
        # self.drive_pub = self.create_publisher(...)

        # Tunable parameters — the autograder doesn't care about exact values,
        # only about algorithm shape. Tune them by pushing and reading the result.
        self.bubble_radius_m = 0.30   # meters; safety bubble around closest point
        self.max_range_m = 3.0        # cap LiDAR readings at this distance
        self.field_of_view_rad = math.radians(135.0)  # ignore beams behind the car
        self.window_size = 5          # smoothing window for preprocess_lidar
        self.base_speed = 1.5         # m/s

    def preprocess_lidar(self, ranges):
        """Smooth + clamp the LiDAR scan.

        Expected behavior:
          - Replace nan / inf with 0.0 (or skip them in the smoothing window).
          - Apply a moving-average smoothing window of size `self.window_size`.
          - Clip values above `self.max_range_m` to `self.max_range_m`.

        Returns: numpy array of the same length as `ranges`.
        """
        # TODO: implement smoothing + clamping
        return np.asarray(ranges, dtype=np.float32)

    def find_max_gap(self, free_space_ranges):
        """Return (start_i, end_i) of the longest run of nonzero entries in
        `free_space_ranges`. Both indices inclusive.

        If there is no gap (all zeros), return (0, len(...)-1) — the
        autograder treats that as a hint to fall back to "go straight."
        """
        # TODO: implement
        return 0, len(free_space_ranges) - 1

    def find_best_point(self, start_i, end_i, ranges):
        """Pick the index inside [start_i, end_i] that the car should aim
        at. Naive choice: argmax(ranges[start_i:end_i+1]). A "better"
        choice (per lecture): the midpoint of the deepest sub-gap.
        """
        # TODO: implement
        return (start_i + end_i) // 2

    def lidar_callback(self, data):
        """Process each LaserScan and publish an AckermannDriveStamped."""
        ranges = self.preprocess_lidar(data.ranges)

        # TODO: find the closest LiDAR point.
        # TODO: zero out a "safety bubble" of radius `self.bubble_radius_m` (in
        #       beam-index units; convert via data.angle_increment) around
        #       that point. Replace ranges in the bubble with 0.0.
        # TODO: find_max_gap on the bubble-masked array → (start_i, end_i)
        # TODO: find_best_point(start_i, end_i, ranges) → target beam index
        # TODO: convert target index → steering angle =
        #       data.angle_min + target_i * data.angle_increment
        # TODO: scale speed by |steering|: e.g.,
        #       |steer| < 10 deg → self.base_speed
        #       |steer| < 20 deg → self.base_speed * 0.7
        #       else            → self.base_speed * 0.5
        # TODO: build AckermannDriveStamped, set .drive.steering_angle +
        #       .drive.speed, self.drive_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ReactiveFollowGap()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
