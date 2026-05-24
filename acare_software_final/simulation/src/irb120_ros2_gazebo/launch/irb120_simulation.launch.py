#!/usr/bin/python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import xacro
import yaml

def generate_launch_description():

    irb120_ros2_gazebo = os.path.join(
        get_package_share_directory('irb120_ros2_gazebo'),
        'worlds',
        'irb120.world')

    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', irb120_ros2_gazebo],
        output='screen'
    )

    print("")
    print(" --- Cranfield University --- ")
    print("        (c) IFRA Group        ")
    print("")
    print("ros2_RobotSimulation --> ABB IRB-120")
    print("Launch file -> irb120_simulation.launch.py")
    print("")
    print("Robot configuration:")
    print("")

    print("- Cell layout:")
    error = True
    while (error == True):
        print("     + Option N1: ABB IRB-120 alone.")
        print("     + Option N2: ABB IRB-120 in Cranfield University cell.")
        print("     + Option N3: ABB IRB-120 Pick&Place Use-Case.")
        cell_layout = input("  Please select: ")
        if (cell_layout == "1"):
            error = False
            cell_layout_1 = "true"
            cell_layout_2 = "false"
            cell_layout_3 = "false"
        elif (cell_layout == "2"):
            error = False
            cell_layout_1 = "false"
            cell_layout_2 = "true"
            cell_layout_3 = "false"
        elif (cell_layout == "3"):
            error = False
            cell_layout_1 = "false"
            cell_layout_2 = "false"
            cell_layout_3 = "true"
        else:
            print("  Please select a valid option!")
    print("")

    print("- End-effector:")
    error = True
    while (error == True):
        print("     + Option N1: No end-effector.")
        print("     + Option N2: Schunk EGP-64 parallel gripper.")
        end_effector = input("  Please select: ")
        if (end_effector == "1"):
            error = False
            EE_no = "true"
            EE_schunk = "false"
        elif (end_effector == "2"):
            error = False
            EE_no = "false"
            EE_schunk = "true"
        else:
            print("  Please select a valid option!")
    print("")

    irb120_description_path = os.path.join(
        get_package_share_directory('irb120_ros2_gazebo'))
    xacro_file = os.path.join(irb120_description_path, 'urdf', 'irb120.urdf.xacro')
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc, mappings={
        "cell_layout_1": cell_layout_1,
        "cell_layout_2": cell_layout_2,
        "cell_layout_3": cell_layout_3,
        "EE_no": EE_no,
        "EE_schunk": EE_schunk,
    })
    robot_description_config = doc.toxml()
    robot_description = {'robot_description': robot_description_config}

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'irb120'],
        output='screen'
    )

    # ROS GZ Bridge for Gazebo services
    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/world/default/create@ros_gz_interfaces/srv/SpawnEntity',
            '/world/default/set_pose@ros_gz_interfaces/srv/SetEntityPose',
            '/world/default/remove@ros_gz_interfaces/srv/DeleteEntity',
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
        ros_gz_bridge,
    ])
