from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import LaunchConfiguration
import os
import xacro
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    share_dir = get_package_share_directory('urdf_assembly_6dof_description')

    controller_config = os.path.join(share_dir, 'config',
                                     'urdf_assembly_6dof_controllers.yaml')

    xacro_file = os.path.join(share_dir, 'urdf', 'urdf_assembly_6dof.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_urdf = robot_description_config.toxml()

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'robot_description': robot_urdf,
                     'use_sim_time': True}]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            ])
        ]),
        launch_arguments={
            'gz_args': ['-r -v 4 ', os.path.join(share_dir, 'worlds',
                                                  'pick_and_place.sdf')],
        }.items()
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-topic', 'robot_description',
                   '-name', 'urdf_assembly_6dof',
                   '-world', 'pick_and_place',
                   '-z', '0.05'],
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                   'camera_image@sensor_msgs/msg/Image[gz.msgs.Image',
                   'lidar_scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'],
        output='screen',
        remappings=[
            ('camera_image', '/camera/image_raw'),
            ('lidar_scan', '/scan'),
        ],
    )

    load_controllers = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['joint_state_broadcaster',
                           '--controller-manager', '/controller_manager',
                           '--param-file', controller_config],
            ),
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['arm_controller',
                           '--controller-manager', '/controller_manager',
                           '--param-file', controller_config],
            ),
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['gripper_controller',
                           '--controller-manager', '/controller_manager',
                           '--param-file', controller_config],
            ),
        ]
    )

    return LaunchDescription([
        robot_state_publisher_node,
        gazebo,
        spawn_entity,
        bridge,
        load_controllers,
    ])
