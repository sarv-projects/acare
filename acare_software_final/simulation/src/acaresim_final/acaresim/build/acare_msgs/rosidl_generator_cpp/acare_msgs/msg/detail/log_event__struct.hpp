// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from acare_msgs:msg/LogEvent.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/log_event.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__LOG_EVENT__STRUCT_HPP_
#define ACARE_MSGS__MSG__DETAIL__LOG_EVENT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__acare_msgs__msg__LogEvent __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__msg__LogEvent __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct LogEvent_
{
  using Type = LogEvent_<ContainerAllocator>;

  explicit LogEvent_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->event_type = "";
      this->user_id = "";
      this->tool = "";
      this->state = "";
      this->description = "";
      this->timestamp = 0ll;
      this->voice_e2e_ms = 0ll;
      this->vision_search_ms = 0ll;
      this->motion_ms = 0ll;
      this->total_task_ms = 0ll;
      this->safety_severity = "";
    }
  }

  explicit LogEvent_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : event_type(_alloc),
    user_id(_alloc),
    tool(_alloc),
    state(_alloc),
    description(_alloc),
    safety_severity(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->event_type = "";
      this->user_id = "";
      this->tool = "";
      this->state = "";
      this->description = "";
      this->timestamp = 0ll;
      this->voice_e2e_ms = 0ll;
      this->vision_search_ms = 0ll;
      this->motion_ms = 0ll;
      this->total_task_ms = 0ll;
      this->safety_severity = "";
    }
  }

  // field types and members
  using _event_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _event_type_type event_type;
  using _user_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _user_id_type user_id;
  using _tool_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _tool_type tool;
  using _state_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _state_type state;
  using _description_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _description_type description;
  using _timestamp_type =
    int64_t;
  _timestamp_type timestamp;
  using _voice_e2e_ms_type =
    int64_t;
  _voice_e2e_ms_type voice_e2e_ms;
  using _vision_search_ms_type =
    int64_t;
  _vision_search_ms_type vision_search_ms;
  using _motion_ms_type =
    int64_t;
  _motion_ms_type motion_ms;
  using _total_task_ms_type =
    int64_t;
  _total_task_ms_type total_task_ms;
  using _safety_severity_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _safety_severity_type safety_severity;

  // setters for named parameter idiom
  Type & set__event_type(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->event_type = _arg;
    return *this;
  }
  Type & set__user_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->user_id = _arg;
    return *this;
  }
  Type & set__tool(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->tool = _arg;
    return *this;
  }
  Type & set__state(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->state = _arg;
    return *this;
  }
  Type & set__description(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->description = _arg;
    return *this;
  }
  Type & set__timestamp(
    const int64_t & _arg)
  {
    this->timestamp = _arg;
    return *this;
  }
  Type & set__voice_e2e_ms(
    const int64_t & _arg)
  {
    this->voice_e2e_ms = _arg;
    return *this;
  }
  Type & set__vision_search_ms(
    const int64_t & _arg)
  {
    this->vision_search_ms = _arg;
    return *this;
  }
  Type & set__motion_ms(
    const int64_t & _arg)
  {
    this->motion_ms = _arg;
    return *this;
  }
  Type & set__total_task_ms(
    const int64_t & _arg)
  {
    this->total_task_ms = _arg;
    return *this;
  }
  Type & set__safety_severity(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->safety_severity = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    acare_msgs::msg::LogEvent_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::msg::LogEvent_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::msg::LogEvent_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::msg::LogEvent_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::LogEvent_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::LogEvent_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::LogEvent_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::LogEvent_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::msg::LogEvent_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::msg::LogEvent_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__msg__LogEvent
    std::shared_ptr<acare_msgs::msg::LogEvent_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__msg__LogEvent
    std::shared_ptr<acare_msgs::msg::LogEvent_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LogEvent_ & other) const
  {
    if (this->event_type != other.event_type) {
      return false;
    }
    if (this->user_id != other.user_id) {
      return false;
    }
    if (this->tool != other.tool) {
      return false;
    }
    if (this->state != other.state) {
      return false;
    }
    if (this->description != other.description) {
      return false;
    }
    if (this->timestamp != other.timestamp) {
      return false;
    }
    if (this->voice_e2e_ms != other.voice_e2e_ms) {
      return false;
    }
    if (this->vision_search_ms != other.vision_search_ms) {
      return false;
    }
    if (this->motion_ms != other.motion_ms) {
      return false;
    }
    if (this->total_task_ms != other.total_task_ms) {
      return false;
    }
    if (this->safety_severity != other.safety_severity) {
      return false;
    }
    return true;
  }
  bool operator!=(const LogEvent_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LogEvent_

// alias to use template instance with default allocator
using LogEvent =
  acare_msgs::msg::LogEvent_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__LOG_EVENT__STRUCT_HPP_
