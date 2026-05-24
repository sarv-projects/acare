// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:msg/ArmCommand.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/arm_command.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__ARM_COMMAND__BUILDER_HPP_
#define ACARE_MSGS__MSG__DETAIL__ARM_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/msg/detail/arm_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace msg
{

namespace builder
{

class Init_ArmCommand_blocking
{
public:
  explicit Init_ArmCommand_blocking(::acare_msgs::msg::ArmCommand & msg)
  : msg_(msg)
  {}
  ::acare_msgs::msg::ArmCommand blocking(::acare_msgs::msg::ArmCommand::_blocking_type arg)
  {
    msg_.blocking = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::msg::ArmCommand msg_;
};

class Init_ArmCommand_accel_limit
{
public:
  explicit Init_ArmCommand_accel_limit(::acare_msgs::msg::ArmCommand & msg)
  : msg_(msg)
  {}
  Init_ArmCommand_blocking accel_limit(::acare_msgs::msg::ArmCommand::_accel_limit_type arg)
  {
    msg_.accel_limit = std::move(arg);
    return Init_ArmCommand_blocking(msg_);
  }

private:
  ::acare_msgs::msg::ArmCommand msg_;
};

class Init_ArmCommand_velocity_scale
{
public:
  explicit Init_ArmCommand_velocity_scale(::acare_msgs::msg::ArmCommand & msg)
  : msg_(msg)
  {}
  Init_ArmCommand_accel_limit velocity_scale(::acare_msgs::msg::ArmCommand::_velocity_scale_type arg)
  {
    msg_.velocity_scale = std::move(arg);
    return Init_ArmCommand_accel_limit(msg_);
  }

private:
  ::acare_msgs::msg::ArmCommand msg_;
};

class Init_ArmCommand_joint_angles
{
public:
  explicit Init_ArmCommand_joint_angles(::acare_msgs::msg::ArmCommand & msg)
  : msg_(msg)
  {}
  Init_ArmCommand_velocity_scale joint_angles(::acare_msgs::msg::ArmCommand::_joint_angles_type arg)
  {
    msg_.joint_angles = std::move(arg);
    return Init_ArmCommand_velocity_scale(msg_);
  }

private:
  ::acare_msgs::msg::ArmCommand msg_;
};

class Init_ArmCommand_command
{
public:
  Init_ArmCommand_command()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ArmCommand_joint_angles command(::acare_msgs::msg::ArmCommand::_command_type arg)
  {
    msg_.command = std::move(arg);
    return Init_ArmCommand_joint_angles(msg_);
  }

private:
  ::acare_msgs::msg::ArmCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::msg::ArmCommand>()
{
  return acare_msgs::msg::builder::Init_ArmCommand_command();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__ARM_COMMAND__BUILDER_HPP_
