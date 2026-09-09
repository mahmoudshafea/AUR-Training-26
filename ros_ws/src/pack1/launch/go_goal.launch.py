import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

#The launch file is a manager that starts all the nodes for you


def generate_launch_description():
    # Find the path to the installed YAML file
    pkg_share = get_package_share_directory('pack1')
    param_file = os.path.join(pkg_share, 'config', 'go_to_goal_params.yaml')

    # Define the node execution
    demo_node = Node(
        package='pack1',
        executable='go_to_goal',
        name='go_to_goal',
        output='screen',
        parameters=[param_file]
    )

    client_node = Node(
        package='pack1',
        executable='go_to_goal_client',
        name='go_to_goal_client',
        output='screen',
        parameters=[param_file]
    )

    turtle_node=Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim',
        output='screen',
        parameters=[param_file]

    )


    return LaunchDescription([
        demo_node,
        client_node,
        turtle_node
    ])