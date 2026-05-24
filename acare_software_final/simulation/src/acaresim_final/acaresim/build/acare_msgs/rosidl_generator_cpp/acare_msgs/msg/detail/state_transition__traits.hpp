// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from acare_msgs:msg/StateTransition.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/state_transition.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__TRAITS_HPP_
#define ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "acare_msgs/msg/detail/state_transition__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace acare_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const StateTransition & msg,
  std::ostream & out)
{
  out << "{";
  // member: target_state
  {
    out << "target_state: ";
    rosidl_generator_traits::value_to_yaml(msg.target_state, out);
    out << ", ";
  }

  // member: reason
  {
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const StateTransition & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: target_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_state: ";
    rosidl_generator_traits::value_to_yaml(msg.target_state, out);
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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const StateTransition & msg, bool use_flow_style = false)
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
  const acare_msgs::msg::StateTransition & msg,
  std::ostream & out, size_t indentation = 0)
{
  acare_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use acare_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const acare_msgs::msg::StateTransition & msg)
{
  return acare_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<acare_msgs::msg::StateTransition>()
{
  return "acare_msgs::msg::StateTransition";
}

template<>
inline const char * name<acare_msgs::msg::StateTransition>()
{
  return "acare_msgs/msg/StateTransition";
}

template<>
struct has_fixed_size<acare_msgs::msg::StateTransition>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<acare_msgs::msg::StateTransition>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<acare_msgs::msg::StateTransition>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__TRAITS_HPP_
