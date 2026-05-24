import os
import xacro
import yaml
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    desc_pkg = get_package_share_directory('urdf_assembly_6dof_description')
    moveit_pkg = get_package_share_directory('acare_moveit_config')

    controller_config = os.path.join(desc_pkg, 'config',
                                     'urdf_assembly_6dof_controllers.yaml')

    xacro_file = os.path.join(desc_pkg, 'urdf', 'urdf_assembly_6dof.xacro')
    srdf_file = os.path.join(moveit_pkg, 'config', 'urdf_assembly_6dof.srdf')
    kinematics_file = os.path.join(moveit_pkg, 'config', 'kinematics.yaml')
    ompl_file = os.path.join(moveit_pkg, 'config', 'ompl_planning.yaml')

    with open(kinematics_file) as f:
        kinematics = yaml.safe_load(f)
    with open(ompl_file) as f:
        ompl = yaml.safe_load(f)

    robot_desc = xacro.process_file(xacro_file).toxml()

    with open(srdf_file) as f:
        robot_desc_semantic = f.read()

    move_group_params = {
        'robot_description': robot_desc,
        'robot_description_semantic': robot_desc_semantic,
        'robot_description_kinematics': kinematics,
        'planning_pipelines': ['ompl'],
        'default_planning_pipeline': 'ompl',
        'ompl': ompl,
        'use_sim_time': True,
        'publish_robot_description': True,
        'publish_robot_description_semantic': True,
        'moveit_manage_controllers': True,
        'moveit_simple_controller_manager': {
            'controller_names': ['arm_controller', 'gripper_controller'],
            'arm_controller': {
                'type': 'FollowJointTrajectory',
                'action_ns': 'follow_joint_trajectory',
                'default': True,
                'joints': ['base', 'shoulder', 'elbow', 'wrist_1', 'wrist_2', 'wrist_3'],
            },
            'gripper_controller': {
                'type': 'FollowJointTrajectory',
                'action_ns': 'follow_joint_trajectory',
                'default': True,
                'joints': ['gripper_slider_left', 'gripper_slider_right'],
            },
        },
    }

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch', 'gz_sim.launch.py'
            ])
        ]),
        launch_arguments={
            'gz_args': ['-r -v 4 ', os.path.join(desc_pkg, 'worlds',
                                                   'pick_and_place.sdf')],
        }.items()
    )

    spawn_entity = Node(
        package='ros_gz_sim', executable='create', output='screen',
        arguments=['-topic', 'robot_description',
                   '-name', 'urdf_assembly_6dof',
                   '-world', 'pick_and_place',
                   '-z', '0.05'],
    )

    bridge = Node(
        package='ros_gz_bridge', executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                   'camera_image@sensor_msgs/msg/Image[gz.msgs.Image',
                   'lidar_scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'],
        output='screen',
        remappings=[
            ('camera_image', '/camera/image_raw'),
            ('lidar_scan', '/scan'),
        ],
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher', executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}],
    )

    move_group_node = Node(
        package='moveit_ros_move_group', executable='move_group',
        output='screen', parameters=[move_group_params],
    )

    rviz_node = Node(
        package='rviz2', executable='rviz2', output='screen',
        parameters=[move_group_params],
    )

    load_controllers = TimerAction(
        period=5.0,
        actions=[
            Node(package='controller_manager', executable='spawner',
                 arguments=['joint_state_broadcaster',
                            '--controller-manager', '/controller_manager',
                            '--param-file', controller_config]),
            Node(package='controller_manager', executable='spawner',
                 arguments=['arm_controller',
                            '--controller-manager', '/controller_manager',
                            '--param-file', controller_config]),
            Node(package='controller_manager', executable='spawner',
                 arguments=['gripper_controller',
                            '--controller-manager', '/controller_manager',
                            '--param-file', controller_config]),
        ]
    )

    return LaunchDescription([
        gazebo,
        spawn_entity,
        bridge,
        robot_state_publisher_node,
        move_group_node,
        rviz_node,
        load_controllers,
    ])
