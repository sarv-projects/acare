// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:msg/RobotState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/robot_state.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_
#define ACARE_MSGS__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/msg/detail/robot_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace msg
{

namespace builder
{

class Init_RobotState_active_user_id
{
public:
  explicit Init_RobotState_active_user_id(::acare_msgs::msg::RobotState & msg)
  : msg_(msg)
  {}
  ::acare_msgs::msg::RobotState active_user_id(::acare_msgs::msg::RobotState::_active_user_id_type arg)
  {
    msg_.active_user_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::msg::RobotState msg_;
};

class Init_RobotState_state
{
public:
  Init_RobotState_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotState_active_user_id state(::acare_msgs::msg::RobotState::_state_type arg)
  {
    msg_.state = std::move(arg);
    return Init_RobotState_active_user_id(msg_);
  }

private:
  ::acare_msgs::msg::RobotState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::msg::RobotState>()
{
  return acare_msgs::msg::builder::Init_RobotState_state();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_
