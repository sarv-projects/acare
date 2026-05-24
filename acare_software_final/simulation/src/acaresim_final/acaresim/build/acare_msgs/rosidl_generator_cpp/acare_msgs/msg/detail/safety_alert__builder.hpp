// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:msg/SafetyAlert.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/safety_alert.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__SAFETY_ALERT__BUILDER_HPP_
#define ACARE_MSGS__MSG__DETAIL__SAFETY_ALERT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/msg/detail/safety_alert__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace msg
{

namespace builder
{

class Init_SafetyAlert_source
{
public:
  explicit Init_SafetyAlert_source(::acare_msgs::msg::SafetyAlert & msg)
  : msg_(msg)
  {}
  ::acare_msgs::msg::SafetyAlert source(::acare_msgs::msg::SafetyAlert::_source_type arg)
  {
    msg_.source = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::msg::SafetyAlert msg_;
};

class Init_SafetyAlert_reason
{
public:
  explicit Init_SafetyAlert_reason(::acare_msgs::msg::SafetyAlert & msg)
  : msg_(msg)
  {}
  Init_SafetyAlert_source reason(::acare_msgs::msg::SafetyAlert::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return Init_SafetyAlert_source(msg_);
  }

private:
  ::acare_msgs::msg::SafetyAlert msg_;
};

class Init_SafetyAlert_severity
{
public:
  Init_SafetyAlert_severity()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SafetyAlert_reason severity(::acare_msgs::msg::SafetyAlert::_severity_type arg)
  {
    msg_.severity = std::move(arg);
    return Init_SafetyAlert_reason(msg_);
  }

private:
  ::acare_msgs::msg::SafetyAlert msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::msg::SafetyAlert>()
{
  return acare_msgs::msg::builder::Init_SafetyAlert_severity();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__SAFETY_ALERT__BUILDER_HPP_
