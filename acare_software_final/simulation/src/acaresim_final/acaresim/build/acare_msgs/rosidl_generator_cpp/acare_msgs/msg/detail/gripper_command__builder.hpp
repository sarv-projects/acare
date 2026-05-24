// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:msg/GripperCommand.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/gripper_command.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__GRIPPER_COMMAND__BUILDER_HPP_
#define ACARE_MSGS__MSG__DETAIL__GRIPPER_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/msg/detail/gripper_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace msg
{

namespace builder
{

class Init_GripperCommand_force_target
{
public:
  explicit Init_GripperCommand_force_target(::acare_msgs::msg::GripperCommand & msg)
  : msg_(msg)
  {}
  ::acare_msgs::msg::GripperCommand force_target(::acare_msgs::msg::GripperCommand::_force_target_type arg)
  {
    msg_.force_target = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::msg::GripperCommand msg_;
};

class Init_GripperCommand_command
{
public:
  Init_GripperCommand_command()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GripperCommand_force_target command(::acare_msgs::msg::GripperCommand::_command_type arg)
  {
    msg_.command = std::move(arg);
    return Init_GripperCommand_force_target(msg_);
  }

private:
  ::acare_msgs::msg::GripperCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::msg::GripperCommand>()
{
  return acare_msgs::msg::builder::Init_GripperCommand_command();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__GRIPPER_COMMAND__BUILDER_HPP_
