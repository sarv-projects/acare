// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:msg/ValidatedIntent.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/validated_intent.h"


#ifndef ACARE_MSGS__MSG__DETAIL__VALIDATED_INTENT__STRUCT_H_
#define ACARE_MSGS__MSG__DETAIL__VALIDATED_INTENT__STRUCT_H_

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
// Member 'user_id'
// Member 'name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/ValidatedIntent in the package acare_msgs.
typedef struct acare_msgs__msg__ValidatedIntent
{
  rosidl_runtime_c__String tool;
  rosidl_runtime_c__String action;
  rosidl_runtime_c__String user_id;
  rosidl_runtime_c__String name;
  bool authenticated;
} acare_msgs__msg__ValidatedIntent;

// Struct for a sequence of acare_msgs__msg__ValidatedIntent.
typedef struct acare_msgs__msg__ValidatedIntent__Sequence
{
  acare_msgs__msg__ValidatedIntent * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__msg__ValidatedIntent__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__VALIDATED_INTENT__STRUCT_H_
