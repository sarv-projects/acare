# acare_bringup/qos_profiles.py
# Spec Reference: Section V (ROS2 QoS Policy)
#
# Centralised QoS profiles for all ACARE nodes.
# Import this module wherever a publisher or subscriber is created.
#
# Spec-mandated policy table:
#   Sensor data (/motion_feedback, /lidar_scan)      → BEST_EFFORT  (drop stale, always use latest)
#   Commands (/arm_command, /gripper_command,         → RELIABLE     (never drop)
#             /emergency_stop)
#   State topics (/robot_state, /state_transition,   → RELIABLE     (all nodes must see changes)
#                 /safety_alert)
#   Logging (/log_event)                             → BEST_EFFORT  (loss acceptable; never block)
#   Vision results (/vision_result, /vision_status,  → RELIABLE     (planner must receive result)
#                   /hand_status)

from rclpy.qos import (
    QoSProfile,
    ReliabilityPolicy,
    DurabilityPolicy,
    HistoryPolicy,
)


# ---------------------------------------------------------------------------
# BEST_EFFORT — sensor data / logging
# Always deliver the latest; stale values can be dropped without retransmit.
# ---------------------------------------------------------------------------
SENSOR_QOS = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
    history=HistoryPolicy.KEEP_LAST,
    depth=10,
)

# For high-rate sensor topics (50 Hz MCU telemetry) use depth=1 to only
# keep the absolute latest sample in the queue.
SENSOR_QOS_DEPTH1 = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
)

# ---------------------------------------------------------------------------
# RELIABLE — commands / state / vision results
# Guaranteed delivery; retransmit until acknowledged.
# ---------------------------------------------------------------------------
RELIABLE_QOS = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.VOLATILE,
    history=HistoryPolicy.KEEP_LAST,
    depth=10,
)

# For /robot_state — late-joining nodes need the last published state.
# TRANSIENT_LOCAL ensures they receive the most recent state on subscribe.
STATE_QOS = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
)

# For /emergency_stop — late-joining nodes MUST see active ESTOP state.
# TRANSIENT_LOCAL ensures they receive the last ESTOP signal on subscribe.
ESTOP_QOS = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
)

# ---------------------------------------------------------------------------
# Convenience aliases matching spec names
# ---------------------------------------------------------------------------

# /motion_feedback, /lidar_scan
TOPIC_SENSOR         = SENSOR_QOS_DEPTH1

# /arm_command, /gripper_command
TOPIC_COMMAND        = RELIABLE_QOS

# /emergency_stop (TRANSIENT_LOCAL for late-joining nodes)
TOPIC_ESTOP          = ESTOP_QOS

# /robot_state, /state_transition, /safety_alert
TOPIC_STATE          = STATE_QOS

# /log_event
TOPIC_LOGGING        = SENSOR_QOS

# /vision_result, /vision_status, /hand_status, /vision_search_request
TOPIC_VISION         = RELIABLE_QOS

# /raw_transcript, /intent_result, /validated_intent, /auth_result, /auth_request
TOPIC_VOICE_PIPELINE = RELIABLE_QOS

# /tts_request
TOPIC_TTS            = RELIABLE_QOS
