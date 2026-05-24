// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:msg/StateTransition.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/state_transition.h"


#ifndef ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__STRUCT_H_
#define ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'target_state'
// Member 'reason'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/StateTransition in the package acare_msgs.
typedef struct acare_msgs__msg__StateTransition
{
  rosidl_runtime_c__String target_state;
  rosidl_runtime_c__String reason;
} acare_msgs__msg__StateTransition;

// Struct for a sequence of acare_msgs__msg__StateTransition.
typedef struct acare_msgs__msg__StateTransition__Sequence
{
  acare_msgs__msg__StateTransition * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__msg__StateTransition__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__STATE_TRANSITION__STRUCT_H_
