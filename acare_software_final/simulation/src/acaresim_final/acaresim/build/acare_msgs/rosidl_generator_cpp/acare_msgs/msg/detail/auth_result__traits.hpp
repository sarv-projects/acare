// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from acare_msgs:msg/AuthResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/auth_result.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__AUTH_RESULT__TRAITS_HPP_
#define ACARE_MSGS__MSG__DETAIL__AUTH_RESULT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "acare_msgs/msg/detail/auth_result__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace acare_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const AuthResult & msg,
  std::ostream & out)
{
  out << "{";
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

  // member: role
  {
    out << "role: ";
    rosidl_generator_traits::value_to_yaml(msg.role, out);
    out << ", ";
  }

  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: face_verified
  {
    out << "face_verified: ";
    rosidl_generator_traits::value_to_yaml(msg.face_verified, out);
    out << ", ";
  }

  // member: face_confidence
  {
    out << "face_confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.face_confidence, out);
    out << ", ";
  }

  // member: voice_confidence
  {
    out << "voice_confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.voice_confidence, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const AuthResult & msg,
  std::ostream & out, size_t indentation = 0)
{
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

  // member: role
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "role: ";
    rosidl_generator_traits::value_to_yaml(msg.role, out);
    out << "\n";
  }

  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: face_verified
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "face_verified: ";
    rosidl_generator_traits::value_to_yaml(msg.face_verified, out);
    out << "\n";
  }

  // member: face_confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "face_confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.face_confidence, out);
    out << "\n";
  }

  // member: voice_confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "voice_confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.voice_confidence, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const AuthResult & msg, bool use_flow_style = false)
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
  const acare_msgs::msg::AuthResult & msg,
  std::ostream & out, size_t indentation = 0)
{
  acare_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use acare_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const acare_msgs::msg::AuthResult & msg)
{
  return acare_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<acare_msgs::msg::AuthResult>()
{
  return "acare_msgs::msg::AuthResult";
}

template<>
inline const char * name<acare_msgs::msg::AuthResult>()
{
  return "acare_msgs/msg/AuthResult";
}

template<>
struct has_fixed_size<acare_msgs::msg::AuthResult>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<acare_msgs::msg::AuthResult>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<acare_msgs::msg::AuthResult>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ACARE_MSGS__MSG__DETAIL__AUTH_RESULT__TRAITS_HPP_
