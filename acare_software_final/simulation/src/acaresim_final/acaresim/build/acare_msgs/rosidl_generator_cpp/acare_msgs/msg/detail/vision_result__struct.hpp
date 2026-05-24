// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from acare_msgs:msg/VisionResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/vision_result.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__VISION_RESULT__STRUCT_HPP_
#define ACARE_MSGS__MSG__DETAIL__VISION_RESULT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__acare_msgs__msg__VisionResult __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__msg__VisionResult __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VisionResult_
{
  using Type = VisionResult_<ContainerAllocator>;

  explicit VisionResult_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->found = false;
      this->tool = "";
      this->x = 0.0f;
      this->y = 0.0f;
      this->z = 0.0f;
      this->confidence = 0.0f;
      this->zone = "";
    }
  }

  explicit VisionResult_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : tool(_alloc),
    zone(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->found = false;
      this->tool = "";
      this->x = 0.0f;
      this->y = 0.0f;
      this->z = 0.0f;
      this->confidence = 0.0f;
      this->zone = "";
    }
  }

  // field types and members
  using _found_type =
    bool;
  _found_type found;
  using _tool_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _tool_type tool;
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
  using _zone_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _zone_type zone;

  // setters for named parameter idiom
  Type & set__found(
    const bool & _arg)
  {
    this->found = _arg;
    return *this;
  }
  Type & set__tool(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->tool = _arg;
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
  Type & set__zone(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->zone = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    acare_msgs::msg::VisionResult_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::msg::VisionResult_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::msg::VisionResult_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::msg::VisionResult_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::VisionResult_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::VisionResult_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::VisionResult_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::VisionResult_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::msg::VisionResult_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::msg::VisionResult_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__msg__VisionResult
    std::shared_ptr<acare_msgs::msg::VisionResult_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__msg__VisionResult
    std::shared_ptr<acare_msgs::msg::VisionResult_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VisionResult_ & other) const
  {
    if (this->found != other.found) {
      return false;
    }
    if (this->tool != other.tool) {
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
    if (this->zone != other.zone) {
      return false;
    }
    return true;
  }
  bool operator!=(const VisionResult_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VisionResult_

// alias to use template instance with default allocator
using VisionResult =
  acare_msgs::msg::VisionResult_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__VISION_RESULT__STRUCT_HPP_
