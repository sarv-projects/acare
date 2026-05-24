// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from acare_msgs:msg/ArmCommand.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/arm_command.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__ARM_COMMAND__STRUCT_HPP_
#define ACARE_MSGS__MSG__DETAIL__ARM_COMMAND__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__acare_msgs__msg__ArmCommand __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__msg__ArmCommand __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ArmCommand_
{
  using Type = ArmCommand_<ContainerAllocator>;

  explicit ArmCommand_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->command = "";
      this->velocity_scale = 0.0f;
      this->accel_limit = 0.0f;
      this->blocking = false;
    }
  }

  explicit ArmCommand_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : command(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->command = "";
      this->velocity_scale = 0.0f;
      this->accel_limit = 0.0f;
      this->blocking = false;
    }
  }

  // field types and members
  using _command_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _command_type command;
  using _joint_angles_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _joint_angles_type joint_angles;
  using _velocity_scale_type =
    float;
  _velocity_scale_type velocity_scale;
  using _accel_limit_type =
    float;
  _accel_limit_type accel_limit;
  using _blocking_type =
    bool;
  _blocking_type blocking;

  // setters for named parameter idiom
  Type & set__command(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->command = _arg;
    return *this;
  }
  Type & set__joint_angles(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->joint_angles = _arg;
    return *this;
  }
  Type & set__velocity_scale(
    const float & _arg)
  {
    this->velocity_scale = _arg;
    return *this;
  }
  Type & set__accel_limit(
    const float & _arg)
  {
    this->accel_limit = _arg;
    return *this;
  }
  Type & set__blocking(
    const bool & _arg)
  {
    this->blocking = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    acare_msgs::msg::ArmCommand_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::msg::ArmCommand_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::msg::ArmCommand_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::msg::ArmCommand_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::ArmCommand_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::ArmCommand_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::ArmCommand_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::ArmCommand_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::msg::ArmCommand_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::msg::ArmCommand_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__msg__ArmCommand
    std::shared_ptr<acare_msgs::msg::ArmCommand_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__msg__ArmCommand
    std::shared_ptr<acare_msgs::msg::ArmCommand_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ArmCommand_ & other) const
  {
    if (this->command != other.command) {
      return false;
    }
    if (this->joint_angles != other.joint_angles) {
      return false;
    }
    if (this->velocity_scale != other.velocity_scale) {
      return false;
    }
    if (this->accel_limit != other.accel_limit) {
      return false;
    }
    if (this->blocking != other.blocking) {
      return false;
    }
    return true;
  }
  bool operator!=(const ArmCommand_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ArmCommand_

// alias to use template instance with default allocator
using ArmCommand =
  acare_msgs::msg::ArmCommand_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__ARM_COMMAND__STRUCT_HPP_
