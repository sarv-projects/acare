// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from acare_msgs:msg/HandStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/hand_status.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__HAND_STATUS__TRAITS_HPP_
#define ACARE_MSGS__MSG__DETAIL__HAND_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "acare_msgs/msg/detail/hand_status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace acare_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const HandStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: hand_detected
  {
    out << "hand_detected: ";
    rosidl_generator_traits::value_to_yaml(msg.hand_detected, out);
    out << ", ";
  }

  // member: is_open
  {
    out << "is_open: ";
    rosidl_generator_traits::value_to_yaml(msg.is_open, out);
    out << ", ";
  }

  // member: palm_up
  {
    out << "palm_up: ";
    rosidl_generator_traits::value_to_yaml(msg.palm_up, out);
    out << ", ";
  }

  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << ", ";
  }

  // member: z
  {
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << ", ";
  }

  // member: confidence
  {
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const HandStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: hand_detected
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "hand_detected: ";
    rosidl_generator_traits::value_to_yaml(msg.hand_detected, out);
    out << "\n";
  }

  // member: is_open
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_open: ";
    rosidl_generator_traits::value_to_yaml(msg.is_open, out);
    out << "\n";
  }

  // member: palm_up
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "palm_up: ";
    rosidl_generator_traits::value_to_yaml(msg.palm_up, out);
    out << "\n";
  }

  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }

  // member: z
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << "\n";
  }

  // member: confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const HandStatus & msg, bool use_flow_style = false)
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
  const acare_msgs::msg::HandStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  acare_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use acare_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const acare_msgs::msg::HandStatus & msg)
{
  return acare_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<acare_msgs::msg::HandStatus>()
{
  return "acare_msgs::msg::HandStatus";
}

template<>
inline const char * name<acare_msgs::msg::HandStatus>()
{
  return "acare_msgs/msg/HandStatus";
}

template<>
struct has_fixed_size<acare_msgs::msg::HandStatus>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<acare_msgs::msg::HandStatus>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<acare_msgs::msg::HandStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ACARE_MSGS__MSG__DETAIL__HAND_STATUS__TRAITS_HPP_
