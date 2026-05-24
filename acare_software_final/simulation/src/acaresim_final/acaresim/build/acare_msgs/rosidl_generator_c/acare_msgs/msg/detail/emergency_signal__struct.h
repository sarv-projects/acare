// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:msg/EmergencySignal.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/emergency_signal.h"


#ifndef ACARE_MSGS__MSG__DETAIL__EMERGENCY_SIGNAL__STRUCT_H_
#define ACARE_MSGS__MSG__DETAIL__EMERGENCY_SIGNAL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'reason'
// Member 'source'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/EmergencySignal in the package acare_msgs.
typedef struct acare_msgs__msg__EmergencySignal
{
  rosidl_runtime_c__String reason;
  rosidl_runtime_c__String source;
} acare_msgs__msg__EmergencySignal;

// Struct for a sequence of acare_msgs__msg__EmergencySignal.
typedef struct acare_msgs__msg__EmergencySignal__Sequence
{
  acare_msgs__msg__EmergencySignal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__msg__EmergencySignal__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__EMERGENCY_SIGNAL__STRUCT_H_
