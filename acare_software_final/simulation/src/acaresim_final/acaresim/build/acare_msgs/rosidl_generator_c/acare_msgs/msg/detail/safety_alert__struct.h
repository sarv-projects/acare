// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:msg/SafetyAlert.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/safety_alert.h"


#ifndef ACARE_MSGS__MSG__DETAIL__SAFETY_ALERT__STRUCT_H_
#define ACARE_MSGS__MSG__DETAIL__SAFETY_ALERT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'severity'
// Member 'reason'
// Member 'source'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/SafetyAlert in the package acare_msgs.
typedef struct acare_msgs__msg__SafetyAlert
{
  rosidl_runtime_c__String severity;
  rosidl_runtime_c__String reason;
  rosidl_runtime_c__String source;
} acare_msgs__msg__SafetyAlert;

// Struct for a sequence of acare_msgs__msg__SafetyAlert.
typedef struct acare_msgs__msg__SafetyAlert__Sequence
{
  acare_msgs__msg__SafetyAlert * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__msg__SafetyAlert__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__SAFETY_ALERT__STRUCT_H_
