// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from acare_msgs:msg/AuthResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/auth_result.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__AUTH_RESULT__STRUCT_HPP_
#define ACARE_MSGS__MSG__DETAIL__AUTH_RESULT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__acare_msgs__msg__AuthResult __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__msg__AuthResult __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct AuthResult_
{
  using Type = AuthResult_<ContainerAllocator>;

  explicit AuthResult_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->user_id = "";
      this->name = "";
      this->role = "";
      this->success = false;
      this->face_verified = false;
      this->face_confidence = 0.0f;
      this->voice_confidence = 0.0f;
    }
  }

  explicit AuthResult_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : user_id(_alloc),
    name(_alloc),
    role(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->user_id = "";
      this->name = "";
      this->role = "";
      this->success = false;
      this->face_verified = false;
      this->face_confidence = 0.0f;
      this->voice_confidence = 0.0f;
    }
  }

  // field types and members
  using _user_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _user_id_type user_id;
  using _name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _name_type name;
  using _role_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _role_type role;
  using _success_type =
    bool;
  _success_type success;
  using _face_verified_type =
    bool;
  _face_verified_type face_verified;
  using _face_confidence_type =
    float;
  _face_confidence_type face_confidence;
  using _voice_confidence_type =
    float;
  _voice_confidence_type voice_confidence;

  // setters for named parameter idiom
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
  Type & set__role(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->role = _arg;
    return *this;
  }
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__face_verified(
    const bool & _arg)
  {
    this->face_verified = _arg;
    return *this;
  }
  Type & set__face_confidence(
    const float & _arg)
  {
    this->face_confidence = _arg;
    return *this;
  }
  Type & set__voice_confidence(
    const float & _arg)
  {
    this->voice_confidence = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    acare_msgs::msg::AuthResult_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::msg::AuthResult_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::msg::AuthResult_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::msg::AuthResult_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::AuthResult_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::AuthResult_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::AuthResult_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::AuthResult_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::msg::AuthResult_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::msg::AuthResult_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__msg__AuthResult
    std::shared_ptr<acare_msgs::msg::AuthResult_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__msg__AuthResult
    std::shared_ptr<acare_msgs::msg::AuthResult_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const AuthResult_ & other) const
  {
    if (this->user_id != other.user_id) {
      return false;
    }
    if (this->name != other.name) {
      return false;
    }
    if (this->role != other.role) {
      return false;
    }
    if (this->success != other.success) {
      return false;
    }
    if (this->face_verified != other.face_verified) {
      return false;
    }
    if (this->face_confidence != other.face_confidence) {
      return false;
    }
    if (this->voice_confidence != other.voice_confidence) {
      return false;
    }
    return true;
  }
  bool operator!=(const AuthResult_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct AuthResult_

// alias to use template instance with default allocator
using AuthResult =
  acare_msgs::msg::AuthResult_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__AUTH_RESULT__STRUCT_HPP_
