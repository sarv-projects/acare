// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:msg/LogEvent.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/log_event.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__LOG_EVENT__BUILDER_HPP_
#define ACARE_MSGS__MSG__DETAIL__LOG_EVENT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/msg/detail/log_event__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace msg
{

namespace builder
{

class Init_LogEvent_safety_severity
{
public:
  explicit Init_LogEvent_safety_severity(::acare_msgs::msg::LogEvent & msg)
  : msg_(msg)
  {}
  ::acare_msgs::msg::LogEvent safety_severity(::acare_msgs::msg::LogEvent::_safety_severity_type arg)
  {
    msg_.safety_severity = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::msg::LogEvent msg_;
};

class Init_LogEvent_total_task_ms
{
public:
  explicit Init_LogEvent_total_task_ms(::acare_msgs::msg::LogEvent & msg)
  : msg_(msg)
  {}
  Init_LogEvent_safety_severity total_task_ms(::acare_msgs::msg::LogEvent::_total_task_ms_type arg)
  {
    msg_.total_task_ms = std::move(arg);
    return Init_LogEvent_safety_severity(msg_);
  }

private:
  ::acare_msgs::msg::LogEvent msg_;
};

class Init_LogEvent_motion_ms
{
public:
  explicit Init_LogEvent_motion_ms(::acare_msgs::msg::LogEvent & msg)
  : msg_(msg)
  {}
  Init_LogEvent_total_task_ms motion_ms(::acare_msgs::msg::LogEvent::_motion_ms_type arg)
  {
    msg_.motion_ms = std::move(arg);
    return Init_LogEvent_total_task_ms(msg_);
  }

private:
  ::acare_msgs::msg::LogEvent msg_;
};

class Init_LogEvent_vision_search_ms
{
public:
  explicit Init_LogEvent_vision_search_ms(::acare_msgs::msg::LogEvent & msg)
  : msg_(msg)
  {}
  Init_LogEvent_motion_ms vision_search_ms(::acare_msgs::msg::LogEvent::_vision_search_ms_type arg)
  {
    msg_.vision_search_ms = std::move(arg);
    return Init_LogEvent_motion_ms(msg_);
  }

private:
  ::acare_msgs::msg::LogEvent msg_;
};

class Init_LogEvent_voice_e2e_ms
{
public:
  explicit Init_LogEvent_voice_e2e_ms(::acare_msgs::msg::LogEvent & msg)
  : msg_(msg)
  {}
  Init_LogEvent_vision_search_ms voice_e2e_ms(::acare_msgs::msg::LogEvent::_voice_e2e_ms_type arg)
  {
    msg_.voice_e2e_ms = std::move(arg);
    return Init_LogEvent_vision_search_ms(msg_);
  }

private:
  ::acare_msgs::msg::LogEvent msg_;
};

class Init_LogEvent_timestamp
{
public:
  explicit Init_LogEvent_timestamp(::acare_msgs::msg::LogEvent & msg)
  : msg_(msg)
  {}
  Init_LogEvent_voice_e2e_ms timestamp(::acare_msgs::msg::LogEvent::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_LogEvent_voice_e2e_ms(msg_);
  }

private:
  ::acare_msgs::msg::LogEvent msg_;
};

class Init_LogEvent_description
{
public:
  explicit Init_LogEvent_description(::acare_msgs::msg::LogEvent & msg)
  : msg_(msg)
  {}
  Init_LogEvent_timestamp description(::acare_msgs::msg::LogEvent::_description_type arg)
  {
    msg_.description = std::move(arg);
    return Init_LogEvent_timestamp(msg_);
  }

private:
  ::acare_msgs::msg::LogEvent msg_;
};

class Init_LogEvent_state
{
public:
  explicit Init_LogEvent_state(::acare_msgs::msg::LogEvent & msg)
  : msg_(msg)
  {}
  Init_LogEvent_description state(::acare_msgs::msg::LogEvent::_state_type arg)
  {
    msg_.state = std::move(arg);
    return Init_LogEvent_description(msg_);
  }

private:
  ::acare_msgs::msg::LogEvent msg_;
};

class Init_LogEvent_tool
{
public:
  explicit Init_LogEvent_tool(::acare_msgs::msg::LogEvent & msg)
  : msg_(msg)
  {}
  Init_LogEvent_state tool(::acare_msgs::msg::LogEvent::_tool_type arg)
  {
    msg_.tool = std::move(arg);
    return Init_LogEvent_state(msg_);
  }

private:
  ::acare_msgs::msg::LogEvent msg_;
};

class Init_LogEvent_user_id
{
public:
  explicit Init_LogEvent_user_id(::acare_msgs::msg::LogEvent & msg)
  : msg_(msg)
  {}
  Init_LogEvent_tool user_id(::acare_msgs::msg::LogEvent::_user_id_type arg)
  {
    msg_.user_id = std::move(arg);
    return Init_LogEvent_tool(msg_);
  }

private:
  ::acare_msgs::msg::LogEvent msg_;
};

class Init_LogEvent_event_type
{
public:
  Init_LogEvent_event_type()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LogEvent_user_id event_type(::acare_msgs::msg::LogEvent::_event_type_type arg)
  {
    msg_.event_type = std::move(arg);
    return Init_LogEvent_user_id(msg_);
  }

private:
  ::acare_msgs::msg::LogEvent msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::msg::LogEvent>()
{
  return acare_msgs::msg::builder::Init_LogEvent_event_type();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__LOG_EVENT__BUILDER_HPP_
