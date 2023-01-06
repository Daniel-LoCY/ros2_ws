from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='find_edge_pkg',
            namespace='find_edge_pkg1',
            executable='find_edge',
            name='find_edge'
        ),
        Node(
            package='find_edge_pkg',
            namespace='find_edge_pkg1',
            executable='display',
            name='display'
        ),
        # Node(
        #     package='find_edge_pkg',
        #     namespace='find_edge_pkg1',
        #     executable='capture',
        #     name='capture',
        #     # parameters=[{
        #     #     'num': LaunchConfiguration('num')
        #     # }]
        # )
    ])