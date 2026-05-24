// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from acare_msgs:msg/ValidatedIntent.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/validated_intent.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__VALIDATED_INTENT__STRUCT_HPP_
#define ACARE_MSGS__MSG__DETAIL__VALIDATED_INTENT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__acare_msgs__msg__ValidatedIntent __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__msg__ValidatedIntent __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ValidatedIntent_
{
  using Type = ValidatedIntent_<ContainerAllocator>;

  explicit ValidatedIntent_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->tool = "";
      this->action = "";
      this->user_id = "";
      this->name = "";
      this->authenticated = false;
    }
  }

  explicit ValidatedIntent_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : tool(_alloc),
    action(_alloc),
    user_id(_alloc),
    name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->tool = "";
      this->action = "";
      this->user_id = "";
      this->name = "";
      this->authenticated = false;
    }
  }

  // field types and members
  using _tool_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _tool_type tool;
  using _action_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _action_type action;
  using _user_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _user_id_type user_id;
  using _name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _name_type name;
  using _authenticated_type =
    bool;
  _authenticated_type authenticated;

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
  Type & set__user_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->user_id = _arg;
    return *this;
  }
  Type & set__name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->name = _arg;
    return *this;
  }
  Type & set__authenticated(
    const bool & _arg)
  {
    this->authenticated = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    acare_msgs::msg::ValidatedIntent_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::msg::ValidatedIntent_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::msg::ValidatedIntent_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::msg::ValidatedIntent_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::ValidatedIntent_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::ValidatedIntent_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::ValidatedIntent_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::ValidatedIntent_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::msg::ValidatedIntent_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::msg::ValidatedIntent_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__msg__ValidatedIntent
    std::shared_ptr<acare_msgs::msg::ValidatedIntent_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__msg__ValidatedIntent
    std::shared_ptr<acare_msgs::msg::ValidatedIntent_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ValidatedIntent_ & other) const
  {
    if (this->tool != other.tool) {
      return false;
    }
    if (this->action != other.action) {
      return false;
    }
    if (this->user_id != other.user_id) {
      return false;
    }
    if (this->name != other.name) {
      return false;
    }
    if (this->authenticated != other.authenticated) {
      return false;
    }
    return true;
  }
  bool operator!=(const ValidatedIntent_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ValidatedIntent_

// alias to use template instance with default allocator
using ValidatedIntent =
  acare_msgs::msg::ValidatedIntent_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__VALIDATED_INTENT__STRUCT_HPP_
