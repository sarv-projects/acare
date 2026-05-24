// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from acare_msgs:msg/Intent.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/intent.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__INTENT__STRUCT_HPP_
#define ACARE_MSGS__MSG__DETAIL__INTENT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__acare_msgs__msg__Intent __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__msg__Intent __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Intent_
{
  using Type = Intent_<ContainerAllocator>;

  explicit Intent_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->tool = "";
      this->action = "";
      this->destination = "";
      this->confidence = 0.0f;
    }
  }

  explicit Intent_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : tool(_alloc),
    action(_alloc),
    destination(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->tool = "";
      this->action = "";
      this->destination = "";
      this->confidence = 0.0f;
    }
  }

  // field types and members
  using _tool_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _tool_type tool;
  using _action_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _action_type action;
  using _destination_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _destination_type destination;
  using _confidence_type =
    float;
  _confidence_type confidence;

  // setters for named parameter idiom
  Type & set__tool(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->tool = _arg;
    return *this;
  }
  Type & set__action(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->action = _arg;
    return *this;
  }
  Type & set__destination(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->destination = _arg;
    return *this;
  }
  Type & set__confidence(
    const float & _arg)
  {
    this->confidence = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    acare_msgs::msg::Intent_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::msg::Intent_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::msg::Intent_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::msg::Intent_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::Intent_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::Intent_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::Intent_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::Intent_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::msg::Intent_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::msg::Intent_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__msg__Intent
    std::shared_ptr<acare_msgs::msg::Intent_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__msg__Intent
    std::shared_ptr<acare_msgs::msg::Intent_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Intent_ & other) const
  {
    if (this->tool != other.tool) {
      return false;
    }
    if (this->action != other.action) {
      return false;
    }
    if (this->destination != other.destination) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    return true;
  }
  bool operator!=(const Intent_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Intent_

// alias to use template instance with default allocator
using Intent =
  acare_msgs::msg::Intent_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__INTENT__STRUCT_HPP_
