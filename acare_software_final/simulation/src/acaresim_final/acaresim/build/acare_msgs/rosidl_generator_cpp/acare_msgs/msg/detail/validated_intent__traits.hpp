// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from acare_msgs:msg/ValidatedIntent.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/validated_intent.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__VALIDATED_INTENT__TRAITS_HPP_
#define ACARE_MSGS__MSG__DETAIL__VALIDATED_INTENT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "acare_msgs/msg/detail/validated_intent__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace acare_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ValidatedIntent & msg,
  std::ostream & out)
{
  out << "{";
  // member: tool
  {
    out << "tool: ";
    rosidl_generator_traits::value_to_yaml(msg.tool, out);
    out << ", ";
  }

  // member: action
  {
    out << "action: ";
    rosidl_generator_traits::value_to_yaml(msg.action, out);
    out << ", ";
  }

  // member: user_id
  {
    out << "user_id: ";
    rosidl_generator_traits::value_to_yaml(msg.user_id, out);
    out << ", ";
  }

  // member: name
  {
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
    out << ", ";
  }

  // member: authenticated
  {
    out << "authenticated: ";
    rosidl_generator_traits::value_to_yaml(msg.authenticated, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ValidatedIntent & msg,
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

  // member: action
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "action: ";
    rosidl_generator_traits::value_to_yaml(msg.action, out);
    out << "\n";
  }

  // member: user_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "user_id: ";
    rosidl_generator_traits::value_to_yaml(msg.user_id, out);
    out << "\n";
  }

  // member: name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
    out << "\n";
  }

  // member: authenticated
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "authenticated: ";
    rosidl_generator_traits::value_to_yaml(msg.authenticated, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ValidatedIntent & msg, bool use_flow_style = false)
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
  const acare_msgs::msg::ValidatedIntent & msg,
  std::ostream & out, size_t indentation = 0)
{
  acare_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use acare_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const acare_msgs::msg::ValidatedIntent & msg)
{
  return acare_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<acare_msgs::msg::ValidatedIntent>()
{
  return "acare_msgs::msg::ValidatedIntent";
}

template<>
inline const char * name<acare_msgs::msg::ValidatedIntent>()
{
  return "acare_msgs/msg/ValidatedIntent";
}

template<>
struct has_fixed_size<acare_msgs::msg::ValidatedIntent>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<acare_msgs::msg::ValidatedIntent>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<acare_msgs::msg::ValidatedIntent>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ACARE_MSGS__MSG__DETAIL__VALIDATED_INTENT__TRAITS_HPP_
