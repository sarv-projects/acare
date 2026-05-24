// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:msg/GripperCommand.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/gripper_command.h"


#ifndef ACARE_MSGS__MSG__DETAIL__GRIPPER_COMMAND__STRUCT_H_
#define ACARE_MSGS__MSG__DETAIL__GRIPPER_COMMAND__STRUCT_H_

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

/// Struct defined in msg/GripperCommand in the package acare_msgs.
typedef struct acare_msgs__msg__GripperCommand
{
  rosidl_runtime_c__String command;
  float force_target;
} acare_msgs__msg__GripperCommand;

// Struct for a sequence of acare_msgs__msg__GripperCommand.
typedef struct acare_msgs__msg__GripperCommand__Sequence
{
  acare_msgs__msg__GripperCommand * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__msg__GripperCommand__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__GRIPPER_COMMAND__STRUCT_H_
