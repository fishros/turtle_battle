#!/usr/bin/env python3

import rclpy
from rclpy.node import Node


from turtle_battle.turtle_spawner import TurtleSpawner

def main():
    rclpy.init(args=None)
    node = TurtleSpawner()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

