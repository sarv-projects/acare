// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from acare_msgs:msg/RobotState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/robot_state.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__ROBOT_STATE__STRUCT_HPP_
#define ACARE_MSGS__MSG__DETAIL__ROBOT_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__acare_msgs__msg__RobotState __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__msg__RobotState __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct RobotState_
{
  using Type = RobotState_<ContainerAllocator>;

  explicit RobotState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = "";
      this->active_user_id = "";
    }
  }

  explicit RobotState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : state(_alloc),
    active_user_id(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = "";
      this->active_user_id = "";
    }
  }

  // field types and members
  using _state_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _state_type state;
  using _active_user_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _active_user_id_type active_user_id;

  // setters for named parameter idiom
  Type & set__state(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->state = _arg;
    return *this;
  }
  Type & set__active_user_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->active_user_id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    acare_msgs::msg::RobotState_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::msg::RobotState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::msg::RobotState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::msg::RobotState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::RobotState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::RobotState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::RobotState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::RobotState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::msg::RobotState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::msg::RobotState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__msg__RobotState
    std::shared_ptr<acare_msgs::msg::RobotState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__msg__RobotState
    std::shared_ptr<acare_msgs::msg::RobotState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RobotState_ & other) const
  {
    if (this->state != other.state) {
      return false;
    }
    if (this->active_user_id != other.active_user_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const RobotState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RobotState_

// alias to use template instance with default allocator
using RobotState =
  acare_msgs::msg::RobotState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__ROBOT_STATE__STRUCT_HPP_
