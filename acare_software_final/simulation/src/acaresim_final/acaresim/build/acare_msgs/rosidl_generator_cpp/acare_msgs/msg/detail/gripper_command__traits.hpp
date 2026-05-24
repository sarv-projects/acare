// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from acare_msgs:msg/GripperCommand.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/gripper_command.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__GRIPPER_COMMAND__TRAITS_HPP_
#define ACARE_MSGS__MSG__DETAIL__GRIPPER_COMMAND__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "acare_msgs/msg/detail/gripper_command__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace acare_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const GripperCommand & msg,
  std::ostream & out)
{
  out << "{";
  // member: command
  {
    out << "command: ";
    rosidl_generator_traits::value_to_yaml(msg.command, out);
    out << ", ";
  }

  // member: force_target
  {
    out << "force_target: ";
    rosidl_generator_traits::value_to_yaml(msg.force_target, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GripperCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: command
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "command: ";
    rosidl_generator_traits::value_to_yaml(msg.command, out);
    out << "\n";
  }

  // member: force_target
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "force_target: ";
    rosidl_generator_traits::value_to_yaml(msg.force_target, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GripperCommand & msg, bool use_flow_style = false)
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
  const acare_msgs::msg::GripperCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  acare_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use acare_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const acare_msgs::msg::GripperCommand & msg)
{
  return acare_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<acare_msgs::msg::GripperCommand>()
{
  return "acare_msgs::msg::GripperCommand";
}

template<>
inline const char * name<acare_msgs::msg::GripperCommand>()
{
  return "acare_msgs/msg/GripperCommand";
}

template<>
struct has_fixed_size<acare_msgs::msg::GripperCommand>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<acare_msgs::msg::GripperCommand>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<acare_msgs::msg::GripperCommand>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ACARE_MSGS__MSG__DETAIL__GRIPPER_COMMAND__TRAITS_HPP_
