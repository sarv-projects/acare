// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from acare_msgs:msg/StateTransition.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/state_transition.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__STRUCT_HPP_
#define ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__acare_msgs__msg__StateTransition __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__msg__StateTransition __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct StateTransition_
{
  using Type = StateTransition_<ContainerAllocator>;

  explicit StateTransition_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->target_state = "";
      this->reason = "";
    }
  }

  explicit StateTransition_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : target_state(_alloc),
    reason(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->target_state = "";
      this->reason = "";
    }
  }

  // field types and members
  using _target_state_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _target_state_type target_state;
  using _reason_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reason_type reason;

  // setters for named parameter idiom
  Type & set__target_state(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->target_state = _arg;
    return *this;
  }
  Type & set__reason(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->reason = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    acare_msgs::msg::StateTransition_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::msg::StateTransition_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::msg::StateTransition_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::msg::StateTransition_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::StateTransition_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::StateTransition_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::StateTransition_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::StateTransition_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::msg::StateTransition_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::msg::StateTransition_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__msg__StateTransition
    std::shared_ptr<acare_msgs::msg::StateTransition_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__msg__StateTransition
    std::shared_ptr<acare_msgs::msg::StateTransition_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const StateTransition_ & other) const
  {
    if (this->target_state != other.target_state) {
      return false;
    }
    if (this->reason != other.reason) {
      return false;
    }
    return true;
  }
  bool operator!=(const StateTransition_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct StateTransition_

// alias to use template instance with default allocator
using StateTransition =
  acare_msgs::msg::StateTransition_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__STRUCT_HPP_
