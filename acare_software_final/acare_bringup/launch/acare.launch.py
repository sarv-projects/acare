from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package="acare_voice", executable="voice_node", output="screen"),
        Node(package="acare_dialogue", executable="dialogue_node", output="screen"),
        Node(package="acare_auth", executable="auth_node", output="screen"),
        Node(package="acare_planner", executable="state_manager", output="screen"),
        Node(package="acare_planner", executable="planner_node", output="screen"),
        Node(package="acare_embedded_interface", executable="interface_node", output="screen"),
        Node(package="acare_vision", executable="vision_node", output="screen"),
        Node(package="acare_safety", executable="safety_node", output="screen"),
        Node(package="acare_logging", executable="log_node", output="screen"),
        Node(package="acare_admin", executable="admin_node", output="screen"),
    ])
