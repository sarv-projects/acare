// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:msg/ValidatedIntent.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/validated_intent.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__VALIDATED_INTENT__BUILDER_HPP_
#define ACARE_MSGS__MSG__DETAIL__VALIDATED_INTENT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/msg/detail/validated_intent__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace msg
{

namespace builder
{

class Init_ValidatedIntent_authenticated
{
public:
  explicit Init_ValidatedIntent_authenticated(::acare_msgs::msg::ValidatedIntent & msg)
  : msg_(msg)
  {}
  ::acare_msgs::msg::ValidatedIntent authenticated(::acare_msgs::msg::ValidatedIntent::_authenticated_type arg)
  {
    msg_.authenticated = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::msg::ValidatedIntent msg_;
};

class Init_ValidatedIntent_name
{
public:
  explicit Init_ValidatedIntent_name(::acare_msgs::msg::ValidatedIntent & msg)
  : msg_(msg)
  {}
  Init_ValidatedIntent_authenticated name(::acare_msgs::msg::ValidatedIntent::_name_type arg)
  {
    msg_.name = std::move(arg);
    return Init_ValidatedIntent_authenticated(msg_);
  }

private:
  ::acare_msgs::msg::ValidatedIntent msg_;
};

class Init_ValidatedIntent_user_id
{
public:
  explicit Init_ValidatedIntent_user_id(::acare_msgs::msg::ValidatedIntent & msg)
  : msg_(msg)
  {}
  Init_ValidatedIntent_name user_id(::acare_msgs::msg::ValidatedIntent::_user_id_type arg)
  {
    msg_.user_id = std::move(arg);
    return Init_ValidatedIntent_name(msg_);
  }

private:
  ::acare_msgs::msg::ValidatedIntent msg_;
};

class Init_ValidatedIntent_action
{
public:
  explicit Init_ValidatedIntent_action(::acare_msgs::msg::ValidatedIntent & msg)
  : msg_(msg)
  {}
  Init_ValidatedIntent_user_id action(::acare_msgs::msg::ValidatedIntent::_action_type arg)
  {
    msg_.action = std::move(arg);
    return Init_ValidatedIntent_user_id(msg_);
  }

private:
  ::acare_msgs::msg::ValidatedIntent msg_;
};

class Init_ValidatedIntent_tool
{
public:
  Init_ValidatedIntent_tool()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ValidatedIntent_action tool(::acare_msgs::msg::ValidatedIntent::_tool_type arg)
  {
    msg_.tool = std::move(arg);
    return Init_ValidatedIntent_action(msg_);
  }

private:
  ::acare_msgs::msg::ValidatedIntent msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::msg::ValidatedIntent>()
{
  return acare_msgs::msg::builder::Init_ValidatedIntent_tool();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__VALIDATED_INTENT__BUILDER_HPP_
