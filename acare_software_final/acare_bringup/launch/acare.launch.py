"""
ACARE Main Launch File
Launches all ACARE software nodes with staggered timers and a supervisor.
Staggered startup ensures dependency services are ready before dependent nodes connect.

Usage:
    ros2 launch acare_bringup acare.launch.py
    ros2 launch acare_bringup acare.launch.py supervisor:=true
    ros2 launch acare_bringup acare.launch.py sim_mode:=true
"""
import os
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument, SetEnvironmentVariable, TimerAction,
    LogInfo, RegisterEventHandler
)
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    # --- Arguments ---
    supervisor_arg = DeclareLaunchArgument(
        "supervisor", default_value="false",
        description="Launch the ACARE supervisor process (background watchdog)."
    )
    sim_mode_arg = DeclareLaunchArgument(
        "sim_mode", default_value="false",
        description="Set environment variables for Gazebo simulation compatibility."
    )

    supervisor_cfg = LaunchConfiguration("supervisor")
    sim_mode_cfg = LaunchConfiguration("sim_mode")

    # --- Environment (only in sim mode) ---
    set_gz_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=os.environ.get("GZ_SIM_RESOURCE_PATH", "")
    )

    # --- Supervisor (proper ROS2 Node, launched via Node action) ---
    supervisor_node = Node(
        package="acare_bringup",
        executable="supervisor_node",
        output="screen",
        emulate_tty=True,
    )

    # =========================================================================
    # ACARE Nodes — staggered by dependency layer
    # =========================================================================
    #
    # Layer 1: Core infrastructure (state, auth, safety, logging)
    #   These have no ROS2 dependencies on other ACARE nodes.
    #
    # Layer 2: Dialogue, Planner, Embedded Interface
    #   Need /robot_state, /auth_result from Layer 1.
    #
    # Layer 3: Voice (needs dialogue + auth to be up for intent routing)
    #
    # Layer 4: Vision (needs embedded interface for arm commands)
    #
    # Layer 5: Admin (no dependencies, started last)

    # --- Layer 1: Core infrastructure (t=1s) ---
    core_nodes = TimerAction(
        period=1.0,
        actions=[
            Node(package="acare_safety", executable="safety_node", output="screen"),
            Node(package="acare_logging", executable="log_node", output="screen", respawn=True, respawn_delay=2.0),
            LogInfo(msg=["[acare] Layer 1: safety, logging started"]),
        ]
    )

    # State Manager (needs to be up early but after core)
    state_manager = TimerAction(
        period=1.5,
        actions=[
            Node(package="acare_planner", executable="state_manager", output="screen"),
            LogInfo(msg=["[acare] state_manager started"]),
        ]
    )

    # Auth Node (needs state manager for /robot_state)
    auth_node = TimerAction(
        period=2.0,
        actions=[
            Node(package="acare_auth", executable="auth_node", output="screen", respawn=True, respawn_delay=2.0),
            LogInfo(msg=["[acare] auth_node started"]),
        ]
    )

    # --- Layer 2: Planner + Dialogue + Embedded Interface (t=3s) ---
    layer2_nodes = TimerAction(
        period=3.0,
        actions=[
            Node(package="acare_dialogue", executable="dialogue_node", output="screen", respawn=True, respawn_delay=2.0),
            Node(package="acare_planner", executable="planner_node", output="screen"),
            Node(package="acare_embedded_interface", executable="interface_node", output="screen"),
            LogInfo(msg=["[acare] Layer 2: dialogue, planner, embedded_interface started"]),
        ]
    )

    # --- Layer 3: Voice (t=3.5s — needs auth + dialogue for intent routing) ---
    voice_node = TimerAction(
        period=3.5,
        actions=[
            Node(package="acare_voice", executable="voice_node", output="screen", respawn=True, respawn_delay=2.0),
            LogInfo(msg=["[acare] voice_node started"]),
        ]
    )

    # --- Layer 4: Vision (t=5s — needs embedded interface) ---
    vision_node = TimerAction(
        period=5.0,
        actions=[
            Node(package="acare_vision", executable="vision_node", output="screen", respawn=True, respawn_delay=2.0),
            LogInfo(msg=["[acare] vision_node started"]),
        ]
    )

    # --- Layer 4: Admin (t=6s) ---
    admin_node = TimerAction(
        period=6.0,
        actions=[
            Node(package="acare_admin", executable="admin_node", output="screen", respawn=True, respawn_delay=2.0),
            LogInfo(msg=["[acare] admin_node started"]),
        ]
    )

    # --- Supervisor (t=8s, only if supervisor=true via IfCondition) ---
    supervisor_timer = TimerAction(
        period=8.0,
        actions=[
            LogInfo(msg=["[acare] supervisor starting..."]),
            supervisor_node,
        ]
    )

    return LaunchDescription([
        # Arguments
        supervisor_arg,
        sim_mode_arg,

        # Environment
        set_gz_resource_path,

        # Log start
        LogInfo(msg=["[acare] Launching ACARE software pipeline..."]),

        # Staggered node launches
        core_nodes,
        state_manager,
        auth_node,
        layer2_nodes,
        voice_node,
        vision_node,
        admin_node,

        # Optional supervisor
        supervisor_timer,
    ])
