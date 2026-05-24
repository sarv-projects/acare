// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from acare_msgs:msg/MotionFeedback.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/motion_feedback.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__MOTION_FEEDBACK__STRUCT_HPP_
#define ACARE_MSGS__MSG__DETAIL__MOTION_FEEDBACK__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__acare_msgs__msg__MotionFeedback __attribute__((deprecated))
#else
# define DEPRECATED__acare_msgs__msg__MotionFeedback __declspec(deprecated)
#endif

namespace acare_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MotionFeedback_
{
  using Type = MotionFeedback_<ContainerAllocator>;

  explicit MotionFeedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->phase = "";
      this->error = "";
      this->gripper_force = 0.0f;
      this->imu_roll = 0.0f;
      this->imu_pitch = 0.0f;
      this->imu_yaw = 0.0f;
    }
  }

  explicit MotionFeedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : phase(_alloc),
    error(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->phase = "";
      this->error = "";
      this->gripper_force = 0.0f;
      this->imu_roll = 0.0f;
      this->imu_pitch = 0.0f;
      this->imu_yaw = 0.0f;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _phase_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _phase_type phase;
  using _error_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _error_type error;
  using _joint_positions_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _joint_positions_type joint_positions;
  using _joint_velocities_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _joint_velocities_type joint_velocities;
  using _joint_currents_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _joint_currents_type joint_currents;
  using _temperatures_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _temperatures_type temperatures;
  using _gripper_force_type =
    float;
  _gripper_force_type gripper_force;
  using _imu_roll_type =
    float;
  _imu_roll_type imu_roll;
  using _imu_pitch_type =
    float;
  _imu_pitch_type imu_pitch;
  using _imu_yaw_type =
    float;
  _imu_yaw_type imu_yaw;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__phase(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->phase = _arg;
    return *this;
  }
  Type & set__error(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->error = _arg;
    return *this;
  }
  Type & set__joint_positions(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->joint_positions = _arg;
    return *this;
  }
  Type & set__joint_velocities(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->joint_velocities = _arg;
    return *this;
  }
  Type & set__joint_currents(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->joint_currents = _arg;
    return *this;
  }
  Type & set__temperatures(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->temperatures = _arg;
    return *this;
  }
  Type & set__gripper_force(
    const float & _arg)
  {
    this->gripper_force = _arg;
    return *this;
  }
  Type & set__imu_roll(
    const float & _arg)
  {
    this->imu_roll = _arg;
    return *this;
  }
  Type & set__imu_pitch(
    const float & _arg)
  {
    this->imu_pitch = _arg;
    return *this;
  }
  Type & set__imu_yaw(
    const float & _arg)
  {
    this->imu_yaw = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    acare_msgs::msg::MotionFeedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const acare_msgs::msg::MotionFeedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<acare_msgs::msg::MotionFeedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<acare_msgs::msg::MotionFeedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::MotionFeedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::MotionFeedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      acare_msgs::msg::MotionFeedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<acare_msgs::msg::MotionFeedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<acare_msgs::msg::MotionFeedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<acare_msgs::msg::MotionFeedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__acare_msgs__msg__MotionFeedback
    std::shared_ptr<acare_msgs::msg::MotionFeedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__acare_msgs__msg__MotionFeedback
    std::shared_ptr<acare_msgs::msg::MotionFeedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotionFeedback_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->phase != other.phase) {
      return false;
    }
    if (this->error != other.error) {
      return false;
    }
    if (this->joint_positions != other.joint_positions) {
      return false;
    }
    if (this->joint_velocities != other.joint_velocities) {
      return false;
    }
    if (this->joint_currents != other.joint_currents) {
      return false;
    }
    if (this->temperatures != other.temperatures) {
      return false;
    }
    if (this->gripper_force != other.gripper_force) {
      return false;
    }
    if (this->imu_roll != other.imu_roll) {
      return false;
    }
    if (this->imu_pitch != other.imu_pitch) {
      return false;
    }
    if (this->imu_yaw != other.imu_yaw) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotionFeedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotionFeedback_

// alias to use template instance with default allocator
using MotionFeedback =
  acare_msgs::msg::MotionFeedback_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__MOTION_FEEDBACK__STRUCT_HPP_
