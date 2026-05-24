// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from acare_msgs:msg/GripperCommand.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/gripper_command.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__GRIPPER_COMMAND__STRUCT_HPP_
#define ACARE_MSGS__MSG__DETAIL__GRIPPER_COMMAND__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__acare_msgs__msg__GripperCommand __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__msg__GripperCommand __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct GripperCommand_
{
  using Type = GripperCommand_<ContainerAllocator>;

  explicit GripperCommand_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->command = "";
      this->force_target = 0.0f;
    }
  }

  explicit GripperCommand_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : command(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->command = "";
      this->force_target = 0.0f;
    }
  }

  // field types and members
  using _command_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _command_type command;
  using _force_target_type =
    float;
  _force_target_type force_target;

  // setters for named parameter idiom
  Type & set__command(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->command = _arg;
    return *this;
  }
  Type & set__force_target(
    const float & _arg)
  {
    this->force_target = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    acare_msgs::msg::GripperCommand_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::msg::GripperCommand_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::msg::GripperCommand_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::msg::GripperCommand_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::GripperCommand_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::GripperCommand_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::GripperCommand_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::GripperCommand_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::msg::GripperCommand_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::msg::GripperCommand_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__msg__GripperCommand
    std::shared_ptr<acare_msgs::msg::GripperCommand_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__msg__GripperCommand
    std::shared_ptr<acare_msgs::msg::GripperCommand_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GripperCommand_ & other) const
  {
    if (this->command != other.command) {
      return false;
    }
    if (this->force_target != other.force_target) {
      return false;
    }
    return true;
  }
  bool operator!=(const GripperCommand_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GripperCommand_

// alias to use template instance with default allocator
using GripperCommand =
  acare_msgs::msg::GripperCommand_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__GRIPPER_COMMAND__STRUCT_HPP_
