// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:msg/VisionResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/vision_result.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__VISION_RESULT__BUILDER_HPP_
#define ACARE_MSGS__MSG__DETAIL__VISION_RESULT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/msg/detail/vision_result__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace msg
{

namespace builder
{

class Init_VisionResult_zone
{
public:
  explicit Init_VisionResult_zone(::acare_msgs::msg::VisionResult & msg)
  : msg_(msg)
  {}
  ::acare_msgs::msg::VisionResult zone(::acare_msgs::msg::VisionResult::_zone_type arg)
  {
    msg_.zone = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::msg::VisionResult msg_;
};

class Init_VisionResult_confidence
{
public:
  explicit Init_VisionResult_confidence(::acare_msgs::msg::VisionResult & msg)
  : msg_(msg)
  {}
  Init_VisionResult_zone confidence(::acare_msgs::msg::VisionResult::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_VisionResult_zone(msg_);
  }

private:
  ::acare_msgs::msg::VisionResult msg_;
};

class Init_VisionResult_z
{
public:
  explicit Init_VisionResult_z(::acare_msgs::msg::VisionResult & msg)
  : msg_(msg)
  {}
  Init_VisionResult_confidence z(::acare_msgs::msg::VisionResult::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_VisionResult_confidence(msg_);
  }

private:
  ::acare_msgs::msg::VisionResult msg_;
};

class Init_VisionResult_y
{
public:
  explicit Init_VisionResult_y(::acare_msgs::msg::VisionResult & msg)
  : msg_(msg)
  {}
  Init_VisionResult_z y(::acare_msgs::msg::VisionResult::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_VisionResult_z(msg_);
  }

private:
  ::acare_msgs::msg::VisionResult msg_;
};

class Init_VisionResult_x
{
public:
  explicit Init_VisionResult_x(::acare_msgs::msg::VisionResult & msg)
  : msg_(msg)
  {}
  Init_VisionResult_y x(::acare_msgs::msg::VisionResult::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_VisionResult_y(msg_);
  }

private:
  ::acare_msgs::msg::VisionResult msg_;
};

class Init_VisionResult_tool
{
public:
  explicit Init_VisionResult_tool(::acare_msgs::msg::VisionResult & msg)
  : msg_(msg)
  {}
  Init_VisionResult_x tool(::acare_msgs::msg::VisionResult::_tool_type arg)
  {
    msg_.tool = std::move(arg);
    return Init_VisionResult_x(msg_);
  }

private:
  ::acare_msgs::msg::VisionResult msg_;
};

class Init_VisionResult_found
{
public:
  Init_VisionResult_found()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VisionResult_tool found(::acare_msgs::msg::VisionResult::_found_type arg)
  {
    msg_.found = std::move(arg);
    return Init_VisionResult_tool(msg_);
  }

private:
  ::acare_msgs::msg::VisionResult msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::msg::VisionResult>()
{
  return acare_msgs::msg::builder::Init_VisionResult_found();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__VISION_RESULT__BUILDER_HPP_
