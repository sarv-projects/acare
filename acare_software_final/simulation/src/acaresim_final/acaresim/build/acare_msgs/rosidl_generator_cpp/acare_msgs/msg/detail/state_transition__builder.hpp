// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:msg/StateTransition.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/state_transition.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__BUILDER_HPP_
#define ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/msg/detail/state_transition__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace msg
{

namespace builder
{

class Init_StateTransition_reason
{
public:
  explicit Init_StateTransition_reason(::acare_msgs::msg::StateTransition & msg)
  : msg_(msg)
  {}
  ::acare_msgs::msg::StateTransition reason(::acare_msgs::msg::StateTransition::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::msg::StateTransition msg_;
};

class Init_StateTransition_target_state
{
public:
  Init_StateTransition_target_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_StateTransition_reason target_state(::acare_msgs::msg::StateTransition::_target_state_type arg)
  {
    msg_.target_state = std::move(arg);
    return Init_StateTransition_reason(msg_);
  }

private:
  ::acare_msgs::msg::StateTransition msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::msg::StateTransition>()
{
  return acare_msgs::msg::builder::Init_StateTransition_target_state();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__BUILDER_HPP_
