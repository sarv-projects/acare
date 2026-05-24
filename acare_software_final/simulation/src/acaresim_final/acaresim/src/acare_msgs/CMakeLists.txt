cmake_minimum_required(VERSION 3.8)
project(acare_msgs)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotState.msg"
  "msg/StateTransition.msg"
  "msg/Intent.msg"
  "msg/ValidatedIntent.msg"
  "msg/SafetyAlert.msg"
  "msg/HandStatus.msg"
  "msg/AuthResult.msg"
  "msg/VisionResult.msg"
  "msg/VisionSearchRequest.msg"
  "msg/ArmCommand.msg"
  "msg/GripperCommand.msg"
  "msg/MotionFeedback.msg"
  "msg/LogEvent.msg"
  "msg/EmergencySignal.msg"
  "srv/EnrolStaff.srv"
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
