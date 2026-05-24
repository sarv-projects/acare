// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:msg/MotionFeedback.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/motion_feedback.h"


#ifndef ACARE_MSGS__MSG__DETAIL__MOTION_FEEDBACK__STRUCT_H_
#define ACARE_MSGS__MSG__DETAIL__MOTION_FEEDBACK__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'phase'
// Member 'error'
#include "rosidl_runtime_c/string.h"
// Member 'joint_positions'
// Member 'joint_velocities'
// Member 'joint_currents'
// Member 'temperatures'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/MotionFeedback in the package acare_msgs.
typedef struct acare_msgs__msg__MotionFeedback
{
  bool success;
  rosidl_runtime_c__String phase;
  rosidl_runtime_c__String error;
  rosidl_runtime_c__float__Sequence joint_positions;
  rosidl_runtime_c__float__Sequence joint_velocities;
  rosidl_runtime_c__float__Sequence joint_currents;
  rosidl_runtime_c__float__Sequence temperatures;
  float gripper_force;
  float imu_roll;
  float imu_pitch;
  float imu_yaw;
} acare_msgs__msg__MotionFeedback;

// Struct for a sequence of acare_msgs__msg__MotionFeedback.
typedef struct acare_msgs__msg__MotionFeedback__Sequence
{
  acare_msgs__msg__MotionFeedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__msg__MotionFeedback__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__MOTION_FEEDBACK__STRUCT_H_
