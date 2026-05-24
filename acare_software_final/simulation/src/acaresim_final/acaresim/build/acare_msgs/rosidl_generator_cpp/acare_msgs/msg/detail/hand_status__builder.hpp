// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:msg/HandStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/hand_status.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__HAND_STATUS__BUILDER_HPP_
#define ACARE_MSGS__MSG__DETAIL__HAND_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/msg/detail/hand_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace msg
{

namespace builder
{

class Init_HandStatus_confidence
{
public:
  explicit Init_HandStatus_confidence(::acare_msgs::msg::HandStatus & msg)
  : msg_(msg)
  {}
  ::acare_msgs::msg::HandStatus confidence(::acare_msgs::msg::HandStatus::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::msg::HandStatus msg_;
};

class Init_HandStatus_z
{
public:
  explicit Init_HandStatus_z(::acare_msgs::msg::HandStatus & msg)
  : msg_(msg)
  {}
  Init_HandStatus_confidence z(::acare_msgs::msg::HandStatus::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_HandStatus_confidence(msg_);
  }

private:
  ::acare_msgs::msg::HandStatus msg_;
};

class Init_HandStatus_y
{
public:
  explicit Init_HandStatus_y(::acare_msgs::msg::HandStatus & msg)
  : msg_(msg)
  {}
  Init_HandStatus_z y(::acare_msgs::msg::HandStatus::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_HandStatus_z(msg_);
  }

private:
  ::acare_msgs::msg::HandStatus msg_;
};

class Init_HandStatus_x
{
public:
  explicit Init_HandStatus_x(::acare_msgs::msg::HandStatus & msg)
  : msg_(msg)
  {}
  Init_HandStatus_y x(::acare_msgs::msg::HandStatus::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_HandStatus_y(msg_);
  }

private:
  ::acare_msgs::msg::HandStatus msg_;
};

class Init_HandStatus_palm_up
{
public:
  explicit Init_HandStatus_palm_up(::acare_msgs::msg::HandStatus & msg)
  : msg_(msg)
  {}
  Init_HandStatus_x palm_up(::acare_msgs::msg::HandStatus::_palm_up_type arg)
  {
    msg_.palm_up = std::move(arg);
    return Init_HandStatus_x(msg_);
  }

private:
  ::acare_msgs::msg::HandStatus msg_;
};

class Init_HandStatus_is_open
{
public:
  explicit Init_HandStatus_is_open(::acare_msgs::msg::HandStatus & msg)
  : msg_(msg)
  {}
  Init_HandStatus_palm_up is_open(::acare_msgs::msg::HandStatus::_is_open_type arg)
  {
    msg_.is_open = std::move(arg);
    return Init_HandStatus_palm_up(msg_);
  }

private:
  ::acare_msgs::msg::HandStatus msg_;
};

class Init_HandStatus_hand_detected
{
public:
  Init_HandStatus_hand_detected()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_HandStatus_is_open hand_detected(::acare_msgs::msg::HandStatus::_hand_detected_type arg)
  {
    msg_.hand_detected = std::move(arg);
    return Init_HandStatus_is_open(msg_);
  }

private:
  ::acare_msgs::msg::HandStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::msg::HandStatus>()
{
  return acare_msgs::msg::builder::Init_HandStatus_hand_detected();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__HAND_STATUS__BUILDER_HPP_
