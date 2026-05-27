"""
ACARE Level 3 Full Simulation Launch File
Launches EVERYTHING: Gazebo + Robot + Bridge + Controllers + Voice + Planner + Vision + Safety
One command to rule them all.
"""
import os
import yaml
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable, TimerAction
)
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro


def generate_launch_description():
    # --- Paths ---
    moveit_pkg = get_package_share_directory("urdf_assembly_6dof_moveit_config")
    desc_pkg = get_package_share_directory("urdf_assembly_6dof_description")

    # --- Process URDF ---
    urdf_file = os.path.join(moveit_pkg, "config", "urdf_assembly_6dof.urdf.xacro")
    robot_description = xacro.process_file(urdf_file).toxml()

    # --- Load SRDF ---
    srdf_file = os.path.join(moveit_pkg, "config", "urdf_assembly_6dof.srdf")
    with open(srdf_file, "r") as f:
        robot_description_semantic = f.read()

    # --- World file ---
    world_file = os.path.join(desc_pkg, "worlds", "acare_ot.sdf")

    # --- Bridge config ---
    bridge_config = os.path.join(desc_pkg, "config", "gz_bridge.yaml")

    # --- Controllers config ---
    controllers_file = os.path.join(moveit_pkg, "config", "ros2_controllers.yaml")

    # --- Set Gazebo plugin path so it finds gz_ros2_control ---
    set_gz_plugin_path = SetEnvironmentVariable(
        name="GZ_SIM_SYSTEM_PLUGIN_PATH",
        value="/opt/ros/jazzy/lib"
    )

    # --- Set GZ_SIM_RESOURCE_PATH for meshes ---
    set_gz_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=os.path.join(desc_pkg, "meshes") + ":" + desc_pkg
    )

    # =========================================================================
    # LAYER 1: GAZEBO + ROBOT
    # =========================================================================

    # Gazebo simulator with the OT world
    gazebo = ExecuteProcess(
        cmd=["gz", "sim", world_file, "-r"],
        output="screen",
        additional_env={"GZ_SIM_SYSTEM_PLUGIN_PATH": "/opt/ros/jazzy/lib"},
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}],
    )

    # Spawn robot into Gazebo
    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=["-topic", "/robot_description", "-name", "acare_arm", "-z", "0.0"],
        output="screen",
    )

    # =========================================================================
    # LAYER 2: ROS-GAZEBO BRIDGE
    # =========================================================================

    # Bridge: Gazebo topics <-> ROS2 topics (camera, LiDAR, clock)
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=["--ros-args", "-p", f"config_file:={bridge_config}"],
        output="screen",
        parameters=[{"use_sim_time": True}],
    )

    # =========================================================================
    # LAYER 3: ROS2 CONTROL (arm + gripper controllers)
    # =========================================================================

    # Controller manager
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {"robot_description": robot_description, "use_sim_time": True},
            controllers_file,
        ],
        output="screen",
    )

    # Spawn controllers (delayed to wait for Gazebo)
    spawn_jsb = ExecuteProcess(
        cmd=["ros2", "control", "load_controller", "--set-state", "active",
             "joint_state_broadcaster"],
        output="screen",
    )
    spawn_arm = ExecuteProcess(
        cmd=["ros2", "control", "load_controller", "--set-state", "active",
             "arm_controller"],
        output="screen",
    )
    spawn_gripper = ExecuteProcess(
        cmd=["ros2", "control", "load_controller", "--set-state", "active",
             "gripper_controller"],
        output="screen",
    )

    # =========================================================================
    # LAYER 4: ACARE SOFTWARE PIPELINE
    # Run as direct Python scripts to avoid entry point packaging issues
    # =========================================================================

    acare_src = os.path.expanduser("~/acare_sim_ws/src")

    # State Manager
    state_manager = ExecuteProcess(
        cmd=["python3", os.path.join(acare_src, "acare_planner", "state_manager.py")],
        output="screen",
    )

    # Planner Node
    planner_node = ExecuteProcess(
        cmd=["python3", os.path.join(acare_src, "acare_planner", "planner_node.py")],
        output="screen",
    )

    # Safety Node
    safety_node = ExecuteProcess(
        cmd=["python3", os.path.join(acare_src, "acare_safety", "safety_node.py")],
        output="screen",
    )

    # Log Node
    log_node = ExecuteProcess(
        cmd=["python3", os.path.join(acare_src, "acare_logging", "log_node.py")],
        output="screen",
    )

    # =========================================================================
    # LAYER 5: RVIZ VISUALIZATION
    # =========================================================================

    rviz_config = os.path.join(moveit_pkg, "config", "moveit.rviz")
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_config] if os.path.exists(rviz_config) else [],
        parameters=[
            {"use_sim_time": True},
            {"robot_description": robot_description},
            {"robot_description_semantic": robot_description_semantic},
        ],
        output="screen",
    )

    # =========================================================================
    # TIMING: Stagger launches so dependencies are ready
    # =========================================================================

    return LaunchDescription([
        # Environment
        set_gz_plugin_path,
        set_gz_resource_path,

        # Layer 1: Gazebo + Robot (immediate)
        gazebo,
        robot_state_publisher,

        # Layer 1b: Spawn robot (after 3s for Gazebo to start)
        TimerAction(period=3.0, actions=[spawn_robot]),

        # Layer 2: Bridge (after 2s)
        TimerAction(period=2.0, actions=[bridge]),

        # Layer 3: Controllers (after 8s for Gazebo plugin to load)
        TimerAction(period=8.0, actions=[spawn_jsb, spawn_arm, spawn_gripper]),

        # Layer 4: ACARE nodes (after 5s)
        TimerAction(period=5.0, actions=[state_manager, safety_node, log_node]),
        TimerAction(period=7.0, actions=[planner_node]),

        # Layer 5: RViz (after 10s)
        TimerAction(period=10.0, actions=[rviz]),
    ])
