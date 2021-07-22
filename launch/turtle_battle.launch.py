from launch import LaunchDescription
from launch_ros.actions import Node



def generate_launch_description():
    ld = LaunchDescription()

    turtlesim_node = Node(
        package="turtlesim",
        executable="turtlesim_node",
        output="own_log"
    )

    turtle_spawner_node  = Node(
        package="turtle_battle",
        executable="turtle_spawner"
    )


    turtle_teleop_key  = Node(
        package="turtlesim",
        executable="turtle_teleop_key"
    )


    ld.add_action(turtlesim_node)
    ld.add_action(turtle_spawner_node)
    # ld.add_action(turtle_teleop_key)

    return ld
