cmake_minimum_required(VERSION 3.8)
project(acare_msgs)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotState.msg"
  "msg/StateTransition.msg"
  "msg/Intent.msg"
  "msg/Transcript.msg"
  "msg/AuthRequest.msg"
  "msg/ValidatedIntent.msg"
  "msg/SafetyAlert.msg"
  "msg/HandStatus.msg"
  "msg/AuthResult.msg"
  "msg/VisionResult.msg"
  "msg/VisionStatus.msg"
  "msg/VisionSearchRequest.msg"
  "msg/ProbabilityUpdate.msg"
  "msg/ArmCommand.msg"
  "msg/GripperCommand.msg"
  "msg/MotionFeedback.msg"
  "msg/LogEvent.msg"
  "msg/EmergencySignal.msg"
  "srv/EnrolStaff.srv"
  DEPENDENCIES std_msgs builtin_interfaces
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
