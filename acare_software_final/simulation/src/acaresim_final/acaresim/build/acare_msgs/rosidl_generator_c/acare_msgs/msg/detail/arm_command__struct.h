// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:msg/ArmCommand.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/arm_command.h"


#ifndef ACARE_MSGS__MSG__DETAIL__ARM_COMMAND__STRUCT_H_
#define ACARE_MSGS__MSG__DETAIL__ARM_COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'command'
#include "rosidl_runtime_c/string.h"
// Member 'joint_angles'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/ArmCommand in the package acare_msgs.
typedef struct acare_msgs__msg__ArmCommand
{
  rosidl_runtime_c__String command;
  rosidl_runtime_c__float__Sequence joint_angles;
  float velocity_scale;
  float accel_limit;
  bool blocking;
} acare_msgs__msg__ArmCommand;

// Struct for a sequence of acare_msgs__msg__ArmCommand.
typedef struct acare_msgs__msg__ArmCommand__Sequence
{
  acare_msgs__msg__ArmCommand * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__msg__ArmCommand__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__ARM_COMMAND__STRUCT_H_
