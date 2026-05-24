// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from acare_msgs:msg/HandStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/hand_status.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__HAND_STATUS__STRUCT_HPP_
#define ACARE_MSGS__MSG__DETAIL__HAND_STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__acare_msgs__msg__HandStatus __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__msg__HandStatus __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct HandStatus_
{
  using Type = HandStatus_<ContainerAllocator>;

  explicit HandStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->hand_detected = false;
      this->is_open = false;
      this->palm_up = false;
      this->x = 0.0f;
      this->y = 0.0f;
      this->z = 0.0f;
      this->confidence = 0.0f;
    }
  }

  explicit HandStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->hand_detected = false;
      this->is_open = false;
      this->palm_up = false;
      this->x = 0.0f;
      this->y = 0.0f;
      this->z = 0.0f;
      this->confidence = 0.0f;
    }
  }

  // field types and members
  using _hand_detected_type =
    bool;
  _hand_detected_type hand_detected;
  using _is_open_type =
    bool;
  _is_open_type is_open;
  using _palm_up_type =
    bool;
  _palm_up_type palm_up;
  using _x_type =
    float;
  _x_type x;
  using _y_type =
    float;
  _y_type y;
  using _z_type =
    float;
  _z_type z;
  using _confidence_type =
    float;
  _confidence_type confidence;

  // setters for named parameter idiom
  Type & set__hand_detected(
    const bool & _arg)
  {
    this->hand_detected = _arg;
    return *this;
  }
  Type & set__is_open(
    const bool & _arg)
  {
    this->is_open = _arg;
    return *this;
  }
  Type & set__palm_up(
    const bool & _arg)
  {
    this->palm_up = _arg;
    return *this;
  }
  Type & set__x(
    const float & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const float & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__z(
    const float & _arg)
  {
    this->z = _arg;
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
    acare_msgs::msg::HandStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::msg::HandStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::msg::HandStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::msg::HandStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::HandStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::HandStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::HandStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::HandStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::msg::HandStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::msg::HandStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__msg__HandStatus
    std::shared_ptr<acare_msgs::msg::HandStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__msg__HandStatus
    std::shared_ptr<acare_msgs::msg::HandStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const HandStatus_ & other) const
  {
    if (this->hand_detected != other.hand_detected) {
      return false;
    }
    if (this->is_open != other.is_open) {
      return false;
    }
    if (this->palm_up != other.palm_up) {
      return false;
    }
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->z != other.z) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    return true;
  }
  bool operator!=(const HandStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct HandStatus_

// alias to use template instance with default allocator
using HandStatus =
  acare_msgs::msg::HandStatus_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__HAND_STATUS__STRUCT_HPP_
