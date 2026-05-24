// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from acare_msgs:msg/EmergencySignal.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/emergency_signal.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__EMERGENCY_SIGNAL__STRUCT_HPP_
#define ACARE_MSGS__MSG__DETAIL__EMERGENCY_SIGNAL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__acare_msgs__msg__EmergencySignal __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__msg__EmergencySignal __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct EmergencySignal_
{
  using Type = EmergencySignal_<ContainerAllocator>;

  explicit EmergencySignal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->reason = "";
      this->source = "";
    }
  }

  explicit EmergencySignal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : reason(_alloc),
    source(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->reason = "";
      this->source = "";
    }
  }

  // field types and members
  using _reason_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reason_type reason;
  using _source_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _source_type source;

  // setters for named parameter idiom
  Type & set__reason(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->reason = _arg;
    return *this;
  }
  Type & set__source(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->source = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    acare_msgs::msg::EmergencySignal_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::msg::EmergencySignal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::msg::EmergencySignal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::msg::EmergencySignal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::EmergencySignal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::EmergencySignal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::EmergencySignal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::EmergencySignal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::msg::EmergencySignal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::msg::EmergencySignal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__msg__EmergencySignal
    std::shared_ptr<acare_msgs::msg::EmergencySignal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__msg__EmergencySignal
    std::shared_ptr<acare_msgs::msg::EmergencySignal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const EmergencySignal_ & other) const
  {
    if (this->reason != other.reason) {
      return false;
    }
    if (this->source != other.source) {
      return false;
    }
    return true;
  }
  bool operator!=(const EmergencySignal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct EmergencySignal_

// alias to use template instance with default allocator
using EmergencySignal =
  acare_msgs::msg::EmergencySignal_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__EMERGENCY_SIGNAL__STRUCT_HPP_
