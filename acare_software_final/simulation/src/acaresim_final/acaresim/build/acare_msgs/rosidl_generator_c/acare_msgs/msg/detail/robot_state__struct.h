// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:msg/RobotState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/robot_state.h"


#ifndef ACARE_MSGS__MSG__DETAIL__ROBOT_STATE__STRUCT_H_
#define ACARE_MSGS__MSG__DETAIL__ROBOT_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'state'
// Member 'active_user_id'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/RobotState in the package acare_msgs.
typedef struct acare_msgs__msg__RobotState
{
  rosidl_runtime_c__String state;
  rosidl_runtime_c__String active_user_id;
} acare_msgs__msg__RobotState;

// Struct for a sequence of acare_msgs__msg__RobotState.
typedef struct acare_msgs__msg__RobotState__Sequence
{
  acare_msgs__msg__RobotState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__msg__RobotState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__ROBOT_STATE__STRUCT_H_
