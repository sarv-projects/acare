// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:msg/Intent.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/intent.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__INTENT__BUILDER_HPP_
#define ACARE_MSGS__MSG__DETAIL__INTENT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/msg/detail/intent__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace msg
{

namespace builder
{

class Init_Intent_confidence
{
public:
  explicit Init_Intent_confidence(::acare_msgs::msg::Intent & msg)
  : msg_(msg)
  {}
  ::acare_msgs::msg::Intent confidence(::acare_msgs::msg::Intent::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::msg::Intent msg_;
};

class Init_Intent_destination
{
public:
  explicit Init_Intent_destination(::acare_msgs::msg::Intent & msg)
  : msg_(msg)
  {}
  Init_Intent_confidence destination(::acare_msgs::msg::Intent::_destination_type arg)
  {
    msg_.destination = std::move(arg);
    return Init_Intent_confidence(msg_);
  }

private:
  ::acare_msgs::msg::Intent msg_;
};

class Init_Intent_action
{
public:
  explicit Init_Intent_action(::acare_msgs::msg::Intent & msg)
  : msg_(msg)
  {}
  Init_Intent_destination action(::acare_msgs::msg::Intent::_action_type arg)
  {
    msg_.action = std::move(arg);
    return Init_Intent_destination(msg_);
  }

private:
  ::acare_msgs::msg::Intent msg_;
};

class Init_Intent_tool
{
public:
  Init_Intent_tool()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Intent_action tool(::acare_msgs::msg::Intent::_tool_type arg)
  {
    msg_.tool = std::move(arg);
    return Init_Intent_action(msg_);
  }

private:
  ::acare_msgs::msg::Intent msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::msg::Intent>()
{
  return acare_msgs::msg::builder::Init_Intent_tool();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__INTENT__BUILDER_HPP_
