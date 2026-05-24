// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:msg/HandStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/hand_status.h"


#ifndef ACARE_MSGS__MSG__DETAIL__HAND_STATUS__STRUCT_H_
#define ACARE_MSGS__MSG__DETAIL__HAND_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Struct defined in msg/HandStatus in the package acare_msgs.
typedef struct acare_msgs__msg__HandStatus
{
  bool hand_detected;
  bool is_open;
  bool palm_up;
  float x;
  float y;
  float z;
  float confidence;
} acare_msgs__msg__HandStatus;

// Struct for a sequence of acare_msgs__msg__HandStatus.
typedef struct acare_msgs__msg__HandStatus__Sequence
{
  acare_msgs__msg__HandStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__msg__HandStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__HAND_STATUS__STRUCT_H_
