// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:msg/VisionSearchRequest.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/vision_search_request.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__VISION_SEARCH_REQUEST__BUILDER_HPP_
#define ACARE_MSGS__MSG__DETAIL__VISION_SEARCH_REQUEST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/msg/detail/vision_search_request__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace msg
{

namespace builder
{

class Init_VisionSearchRequest_tool
{
public:
  Init_VisionSearchRequest_tool()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::acare_msgs::msg::VisionSearchRequest tool(::acare_msgs::msg::VisionSearchRequest::_tool_type arg)
  {
    msg_.tool = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::msg::VisionSearchRequest msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::msg::VisionSearchRequest>()
{
  return acare_msgs::msg::builder::Init_VisionSearchRequest_tool();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__VISION_SEARCH_REQUEST__BUILDER_HPP_
