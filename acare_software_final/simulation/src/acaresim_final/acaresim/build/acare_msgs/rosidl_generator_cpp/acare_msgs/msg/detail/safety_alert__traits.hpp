// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from acare_msgs:msg/SafetyAlert.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/safety_alert.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__SAFETY_ALERT__TRAITS_HPP_
#define ACARE_MSGS__MSG__DETAIL__SAFETY_ALERT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "acare_msgs/msg/detail/safety_alert__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace acare_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const SafetyAlert & msg,
  std::ostream & out)
{
  out << "{";
  // member: severity
  {
    out << "severity: ";
    rosidl_generator_traits::value_to_yaml(msg.severity, out);
    out << ", ";
  }

  // member: reason
  {
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
    out << ", ";
  }

  // member: source
  {
    out << "source: ";
    rosidl_generator_traits::value_to_yaml(msg.source, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SafetyAlert & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: severity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "severity: ";
    rosidl_generator_traits::value_to_yaml(msg.severity, out);
    out << "\n";
  }

  // member: reason
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
    out << "\n";
  }

  // member: source
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "source: ";
    rosidl_generator_traits::value_to_yaml(msg.source, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SafetyAlert & msg, bool use_flow_style = false)
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
  const acare_msgs::msg::SafetyAlert & msg,
  std::ostream & out, size_t indentation = 0)
{
  acare_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use acare_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const acare_msgs::msg::SafetyAlert & msg)
{
  return acare_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<acare_msgs::msg::SafetyAlert>()
{
  return "acare_msgs::msg::SafetyAlert";
}

template<>
inline const char * name<acare_msgs::msg::SafetyAlert>()
{
  return "acare_msgs/msg/SafetyAlert";
}

template<>
struct has_fixed_size<acare_msgs::msg::SafetyAlert>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<acare_msgs::msg::SafetyAlert>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<acare_msgs::msg::SafetyAlert>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ACARE_MSGS__MSG__DETAIL__SAFETY_ALERT__TRAITS_HPP_
