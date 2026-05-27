string command
# Joint-space command: 6 joint angles in radians.
# Used for kiosk poses and any command published with mode == "JOINT".
float32[] joint_angles
# Cartesian-space command: end-effector target in robot base frame.
# pose = [x, y, z, roll, pitch, yaw] in metres / radians.
# Populated for grasp / pregrasp / handover. Empty for joint-space moves.
float32[] pose
# Discriminator. "JOINT" or "CARTESIAN". Defaults to JOINT for backwards
# compatibility with older publishers.
string mode
float32 velocity_scale
float32 accel_limit
bool blocking
