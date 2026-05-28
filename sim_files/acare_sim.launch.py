"""
ACARE Level 3 Full Simulation Launch File
Launches EVERYTHING: Gazebo + Robot + Bridge + Controllers + Voice + Planner + Vision + Safety
One command to rule them all.
"""
import os
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

    # NOTE: With Gazebo's gz_ros2_control plugin, the controller_manager runs
    # INSIDE Gazebo. We do NOT spawn a standalone ros2_control_node here —
    # that would conflict with the in-Gazebo manager.
    # Instead we just spawn the controllers via the spawner once the Gazebo
    # controller_manager service is up.

    spawn_jsb = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="screen",
    )
    spawn_arm = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_controller", "--controller-manager", "/controller_manager"],
        output="screen",
    )
    spawn_gripper = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["gripper_controller", "--controller-manager", "/controller_manager"],
        output="screen",
    )

    # =========================================================================
    # LAYER 4: ACARE SOFTWARE PIPELINE
    # Use entry-point executables installed by colcon (ros2 run equivalents).
    # Relative imports inside these modules require the package to be on
    # PYTHONPATH, which sourcing install/setup.bash provides.
    # =========================================================================

    # State Manager — global FSM
    state_manager = Node(
        package="acare_planner",
        executable="state_manager",
        output="screen",
        parameters=[{"use_sim_time": True}],
    )

    # Planner Node — agentic task planner
    planner_node = Node(
        package="acare_planner",
        executable="planner_node",
        output="screen",
        parameters=[{"use_sim_time": True}],
    )

    # Safety Node — LiDAR + telemetry monitoring
    safety_node = Node(
        package="acare_safety",
        executable="safety_node",
        output="screen",
        parameters=[{"use_sim_time": True}],
    )

    # Log Node — SQLite audit trail
    log_node = Node(
        package="acare_logging",
        executable="log_node",
        output="screen",
        parameters=[{"use_sim_time": True}],
    )

    # Auth Node — biometric authentication (face + voice)
    # demo_mode: true in system.yaml lets users login by saying "confirm"
    # without real face/voice match, but the full auth state machine still runs.
    auth_node = Node(
        package="acare_auth",
        executable="auth_node",
        output="screen",
        parameters=[{"use_sim_time": True}],
    )

    # Dialogue Node — Groq-backed intent parser for /raw_transcript → /intent_result
    # Also drives the LOGGED_OUT conversational agent.
    dialogue_node = Node(
        package="acare_dialogue",
        executable="dialogue_node",
        output="screen",
        parameters=[{"use_sim_time": True}],
    )

    # Embedded Interface — bridges /arm_command → Gazebo's
    # /arm_controller/follow_joint_trajectory action. Without this the arm
    # cannot move in simulation.
    embedded_interface = Node(
        package="acare_embedded_interface",
        executable="interface_node",
        output="screen",
        parameters=[{"use_sim_time": True}],
    )

    # Voice Node — VAD/ASR/TTS/Intent pipeline
    voice_node = Node(
        package="acare_voice",
        executable="voice_node",
        output="screen",
        parameters=[{"use_sim_time": True}],
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

        # Layer 3: Controllers (after 10s for Gazebo plugin to load)
        TimerAction(period=10.0, actions=[spawn_jsb]),
        TimerAction(period=12.0, actions=[spawn_arm, spawn_gripper]),

        # Layer 4: ACARE nodes (after 6s — they need /robot_description)
        TimerAction(period=6.0, actions=[state_manager, safety_node, log_node, auth_node]),
        TimerAction(period=8.0, actions=[planner_node, dialogue_node, embedded_interface]),
        TimerAction(period=14.0, actions=[voice_node]),  # voice last — needs API connections

        # Layer 5: RViz (after 12s)
        TimerAction(period=12.0, actions=[rviz]),
    ])
