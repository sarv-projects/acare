// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from acare_msgs:msg/VisionSearchRequest.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/vision_search_request.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__VISION_SEARCH_REQUEST__TRAITS_HPP_
#define ACARE_MSGS__MSG__DETAIL__VISION_SEARCH_REQUEST__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "acare_msgs/msg/detail/vision_search_request__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace acare_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const VisionSearchRequest & msg,
  std::ostream & out)
{
  out << "{";
  // member: tool
  {
    out << "tool: ";
    rosidl_generator_traits::value_to_yaml(msg.tool, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const VisionSearchRequest & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: tool
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tool: ";
    rosidl_generator_traits::value_to_yaml(msg.tool, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VisionSearchRequest & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace acare_msgs

namespace rosidl_generator_traits
{

[[deprecated("use acare_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const acare_msgs::msg::VisionSearchRequest & msg,
  std::ostream & out, size_t indentation = 0)
{
  acare_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use acare_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const acare_msgs::msg::VisionSearchRequest & msg)
{
  return acare_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<acare_msgs::msg::VisionSearchRequest>()
{
  return "acare_msgs::msg::VisionSearchRequest";
}

template<>
inline const char * name<acare_msgs::msg::VisionSearchRequest>()
{
  return "acare_msgs/msg/VisionSearchRequest";
}

template<>
struct has_fixed_size<acare_msgs::msg::VisionSearchRequest>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<acare_msgs::msg::VisionSearchRequest>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<acare_msgs::msg::VisionSearchRequest>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ACARE_MSGS__MSG__DETAIL__VISION_SEARCH_REQUEST__TRAITS_HPP_
