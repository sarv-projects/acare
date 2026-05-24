// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:msg/EmergencySignal.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/emergency_signal.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__EMERGENCY_SIGNAL__BUILDER_HPP_
#define ACARE_MSGS__MSG__DETAIL__EMERGENCY_SIGNAL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/msg/detail/emergency_signal__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace msg
{

namespace builder
{

class Init_EmergencySignal_source
{
public:
  explicit Init_EmergencySignal_source(::acare_msgs::msg::EmergencySignal & msg)
  : msg_(msg)
  {}
  ::acare_msgs::msg::EmergencySignal source(::acare_msgs::msg::EmergencySignal::_source_type arg)
  {
    msg_.source = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::msg::EmergencySignal msg_;
};

class Init_EmergencySignal_reason
{
public:
  Init_EmergencySignal_reason()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_EmergencySignal_source reason(::acare_msgs::msg::EmergencySignal::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return Init_EmergencySignal_source(msg_);
  }

private:
  ::acare_msgs::msg::EmergencySignal msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::msg::EmergencySignal>()
{
  return acare_msgs::msg::builder::Init_EmergencySignal_reason();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__EMERGENCY_SIGNAL__BUILDER_HPP_
