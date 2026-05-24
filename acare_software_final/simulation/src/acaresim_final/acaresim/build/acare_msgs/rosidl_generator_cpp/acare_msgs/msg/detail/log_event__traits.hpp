// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from acare_msgs:msg/LogEvent.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/log_event.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__LOG_EVENT__TRAITS_HPP_
#define ACARE_MSGS__MSG__DETAIL__LOG_EVENT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "acare_msgs/msg/detail/log_event__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace acare_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const LogEvent & msg,
  std::ostream & out)
{
  out << "{";
  // member: event_type
  {
    out << "event_type: ";
    rosidl_generator_traits::value_to_yaml(msg.event_type, out);
    out << ", ";
  }

  // member: user_id
  {
    out << "user_id: ";
    rosidl_generator_traits::value_to_yaml(msg.user_id, out);
    out << ", ";
  }

  // member: tool
  {
    out << "tool: ";
    rosidl_generator_traits::value_to_yaml(msg.tool, out);
    out << ", ";
  }

  // member: state
  {
    out << "state: ";
    rosidl_generator_traits::value_to_yaml(msg.state, out);
    out << ", ";
  }

  // member: description
  {
    out << "description: ";
    rosidl_generator_traits::value_to_yaml(msg.description, out);
    out << ", ";
  }

  // member: timestamp
  {
    out << "timestamp: ";
    rosidl_generator_traits::value_to_yaml(msg.timestamp, out);
    out << ", ";
  }

  // member: voice_e2e_ms
  {
    out << "voice_e2e_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.voice_e2e_ms, out);
    out << ", ";
  }

  // member: vision_search_ms
  {
    out << "vision_search_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.vision_search_ms, out);
    out << ", ";
  }

  // member: motion_ms
  {
    out << "motion_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.motion_ms, out);
    out << ", ";
  }

  // member: total_task_ms
  {
    out << "total_task_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.total_task_ms, out);
    out << ", ";
  }

  // member: safety_severity
  {
    out << "safety_severity: ";
    rosidl_generator_traits::value_to_yaml(msg.safety_severity, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LogEvent & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: event_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "event_type: ";
    rosidl_generator_traits::value_to_yaml(msg.event_type, out);
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

  // member: tool
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tool: ";
    rosidl_generator_traits::value_to_yaml(msg.tool, out);
    out << "\n";
  }

  // member: state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "state: ";
    rosidl_generator_traits::value_to_yaml(msg.state, out);
    out << "\n";
  }

  // member: description
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "description: ";
    rosidl_generator_traits::value_to_yaml(msg.description, out);
    out << "\n";
  }

  // member: timestamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "timestamp: ";
    rosidl_generator_traits::value_to_yaml(msg.timestamp, out);
    out << "\n";
  }

  // member: voice_e2e_ms
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "voice_e2e_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.voice_e2e_ms, out);
    out << "\n";
  }

  // member: vision_search_ms
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vision_search_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.vision_search_ms, out);
    out << "\n";
  }

  // member: motion_ms
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "motion_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.motion_ms, out);
    out << "\n";
  }

  // member: total_task_ms
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "total_task_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.total_task_ms, out);
    out << "\n";
  }

  // member: safety_severity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "safety_severity: ";
    rosidl_generator_traits::value_to_yaml(msg.safety_severity, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LogEvent & msg, bool use_flow_style = false)
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
  const acare_msgs::msg::LogEvent & msg,
  std::ostream & out, size_t indentation = 0)
{
  acare_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use acare_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const acare_msgs::msg::LogEvent & msg)
{
  return acare_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<acare_msgs::msg::LogEvent>()
{
  return "acare_msgs::msg::LogEvent";
}

template<>
inline const char * name<acare_msgs::msg::LogEvent>()
{
  return "acare_msgs/msg/LogEvent";
}

template<>
struct has_fixed_size<acare_msgs::msg::LogEvent>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<acare_msgs::msg::LogEvent>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<acare_msgs::msg::LogEvent>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ACARE_MSGS__MSG__DETAIL__LOG_EVENT__TRAITS_HPP_
