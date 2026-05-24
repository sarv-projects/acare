// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from acare_msgs:msg/ArmCommand.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/arm_command.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__ARM_COMMAND__TRAITS_HPP_
#define ACARE_MSGS__MSG__DETAIL__ARM_COMMAND__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "acare_msgs/msg/detail/arm_command__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace acare_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ArmCommand & msg,
  std::ostream & out)
{
  out << "{";
  // member: command
  {
    out << "command: ";
    rosidl_generator_traits::value_to_yaml(msg.command, out);
    out << ", ";
  }

  // member: joint_angles
  {
    if (msg.joint_angles.size() == 0) {
      out << "joint_angles: []";
    } else {
      out << "joint_angles: [";
      size_t pending_items = msg.joint_angles.size();
      for (auto item : msg.joint_angles) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: velocity_scale
  {
    out << "velocity_scale: ";
    rosidl_generator_traits::value_to_yaml(msg.velocity_scale, out);
    out << ", ";
  }

  // member: accel_limit
  {
    out << "accel_limit: ";
    rosidl_generator_traits::value_to_yaml(msg.accel_limit, out);
    out << ", ";
  }

  // member: blocking
  {
    out << "blocking: ";
    rosidl_generator_traits::value_to_yaml(msg.blocking, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ArmCommand & msg,
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

  // member: joint_angles
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joint_angles.size() == 0) {
      out << "joint_angles: []\n";
    } else {
      out << "joint_angles:\n";
      for (auto item : msg.joint_angles) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: velocity_scale
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "velocity_scale: ";
    rosidl_generator_traits::value_to_yaml(msg.velocity_scale, out);
    out << "\n";
  }

  // member: accel_limit
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accel_limit: ";
    rosidl_generator_traits::value_to_yaml(msg.accel_limit, out);
    out << "\n";
  }

  // member: blocking
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "blocking: ";
    rosidl_generator_traits::value_to_yaml(msg.blocking, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ArmCommand & msg, bool use_flow_style = false)
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
  const acare_msgs::msg::ArmCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  acare_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use acare_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const acare_msgs::msg::ArmCommand & msg)
{
  return acare_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<acare_msgs::msg::ArmCommand>()
{
  return "acare_msgs::msg::ArmCommand";
}

template<>
inline const char * name<acare_msgs::msg::ArmCommand>()
{
  return "acare_msgs/msg/ArmCommand";
}

template<>
struct has_fixed_size<acare_msgs::msg::ArmCommand>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<acare_msgs::msg::ArmCommand>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<acare_msgs::msg::ArmCommand>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ACARE_MSGS__MSG__DETAIL__ARM_COMMAND__TRAITS_HPP_
