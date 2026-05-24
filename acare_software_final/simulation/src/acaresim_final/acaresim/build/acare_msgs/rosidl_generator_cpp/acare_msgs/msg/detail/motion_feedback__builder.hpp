// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:msg/MotionFeedback.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/motion_feedback.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__MOTION_FEEDBACK__BUILDER_HPP_
#define ACARE_MSGS__MSG__DETAIL__MOTION_FEEDBACK__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/msg/detail/motion_feedback__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace msg
{

namespace builder
{

class Init_MotionFeedback_imu_yaw
{
public:
  explicit Init_MotionFeedback_imu_yaw(::acare_msgs::msg::MotionFeedback & msg)
  : msg_(msg)
  {}
  ::acare_msgs::msg::MotionFeedback imu_yaw(::acare_msgs::msg::MotionFeedback::_imu_yaw_type arg)
  {
    msg_.imu_yaw = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::msg::MotionFeedback msg_;
};

class Init_MotionFeedback_imu_pitch
{
public:
  explicit Init_MotionFeedback_imu_pitch(::acare_msgs::msg::MotionFeedback & msg)
  : msg_(msg)
  {}
  Init_MotionFeedback_imu_yaw imu_pitch(::acare_msgs::msg::MotionFeedback::_imu_pitch_type arg)
  {
    msg_.imu_pitch = std::move(arg);
    return Init_MotionFeedback_imu_yaw(msg_);
  }

private:
  ::acare_msgs::msg::MotionFeedback msg_;
};

class Init_MotionFeedback_imu_roll
{
public:
  explicit Init_MotionFeedback_imu_roll(::acare_msgs::msg::MotionFeedback & msg)
  : msg_(msg)
  {}
  Init_MotionFeedback_imu_pitch imu_roll(::acare_msgs::msg::MotionFeedback::_imu_roll_type arg)
  {
    msg_.imu_roll = std::move(arg);
    return Init_MotionFeedback_imu_pitch(msg_);
  }

private:
  ::acare_msgs::msg::MotionFeedback msg_;
};

class Init_MotionFeedback_gripper_force
{
public:
  explicit Init_MotionFeedback_gripper_force(::acare_msgs::msg::MotionFeedback & msg)
  : msg_(msg)
  {}
  Init_MotionFeedback_imu_roll gripper_force(::acare_msgs::msg::MotionFeedback::_gripper_force_type arg)
  {
    msg_.gripper_force = std::move(arg);
    return Init_MotionFeedback_imu_roll(msg_);
  }

private:
  ::acare_msgs::msg::MotionFeedback msg_;
};

class Init_MotionFeedback_temperatures
{
public:
  explicit Init_MotionFeedback_temperatures(::acare_msgs::msg::MotionFeedback & msg)
  : msg_(msg)
  {}
  Init_MotionFeedback_gripper_force temperatures(::acare_msgs::msg::MotionFeedback::_temperatures_type arg)
  {
    msg_.temperatures = std::move(arg);
    return Init_MotionFeedback_gripper_force(msg_);
  }

private:
  ::acare_msgs::msg::MotionFeedback msg_;
};

class Init_MotionFeedback_joint_currents
{
public:
  explicit Init_MotionFeedback_joint_currents(::acare_msgs::msg::MotionFeedback & msg)
  : msg_(msg)
  {}
  Init_MotionFeedback_temperatures joint_currents(::acare_msgs::msg::MotionFeedback::_joint_currents_type arg)
  {
    msg_.joint_currents = std::move(arg);
    return Init_MotionFeedback_temperatures(msg_);
  }

private:
  ::acare_msgs::msg::MotionFeedback msg_;
};

class Init_MotionFeedback_joint_velocities
{
public:
  explicit Init_MotionFeedback_joint_velocities(::acare_msgs::msg::MotionFeedback & msg)
  : msg_(msg)
  {}
  Init_MotionFeedback_joint_currents joint_velocities(::acare_msgs::msg::MotionFeedback::_joint_velocities_type arg)
  {
    msg_.joint_velocities = std::move(arg);
    return Init_MotionFeedback_joint_currents(msg_);
  }

private:
  ::acare_msgs::msg::MotionFeedback msg_;
};

class Init_MotionFeedback_joint_positions
{
public:
  explicit Init_MotionFeedback_joint_positions(::acare_msgs::msg::MotionFeedback & msg)
  : msg_(msg)
  {}
  Init_MotionFeedback_joint_velocities joint_positions(::acare_msgs::msg::MotionFeedback::_joint_positions_type arg)
  {
    msg_.joint_positions = std::move(arg);
    return Init_MotionFeedback_joint_velocities(msg_);
  }

private:
  ::acare_msgs::msg::MotionFeedback msg_;
};

class Init_MotionFeedback_error
{
public:
  explicit Init_MotionFeedback_error(::acare_msgs::msg::MotionFeedback & msg)
  : msg_(msg)
  {}
  Init_MotionFeedback_joint_positions error(::acare_msgs::msg::MotionFeedback::_error_type arg)
  {
    msg_.error = std::move(arg);
    return Init_MotionFeedback_joint_positions(msg_);
  }

private:
  ::acare_msgs::msg::MotionFeedback msg_;
};

class Init_MotionFeedback_phase
{
public:
  explicit Init_MotionFeedback_phase(::acare_msgs::msg::MotionFeedback & msg)
  : msg_(msg)
  {}
  Init_MotionFeedback_error phase(::acare_msgs::msg::MotionFeedback::_phase_type arg)
  {
    msg_.phase = std::move(arg);
    return Init_MotionFeedback_error(msg_);
  }

private:
  ::acare_msgs::msg::MotionFeedback msg_;
};

class Init_MotionFeedback_success
{
public:
  Init_MotionFeedback_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotionFeedback_phase success(::acare_msgs::msg::MotionFeedback::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MotionFeedback_phase(msg_);
  }

private:
  ::acare_msgs::msg::MotionFeedback msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::msg::MotionFeedback>()
{
  return acare_msgs::msg::builder::Init_MotionFeedback_success();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__MOTION_FEEDBACK__BUILDER_HPP_
