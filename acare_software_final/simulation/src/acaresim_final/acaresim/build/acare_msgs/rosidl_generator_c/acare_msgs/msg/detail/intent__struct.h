// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:msg/Intent.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/intent.h"


#ifndef ACARE_MSGS__MSG__DETAIL__INTENT__STRUCT_H_
#define ACARE_MSGS__MSG__DETAIL__INTENT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'tool'
// Member 'action'
// Member 'destination'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/Intent in the package acare_msgs.
typedef struct acare_msgs__msg__Intent
{
  rosidl_runtime_c__String tool;
  rosidl_runtime_c__String action;
  rosidl_runtime_c__String destination;
  float confidence;
} acare_msgs__msg__Intent;

// Struct for a sequence of acare_msgs__msg__Intent.
typedef struct acare_msgs__msg__Intent__Sequence
{
  acare_msgs__msg__Intent * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__msg__Intent__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__INTENT__STRUCT_H_
