// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:msg/VisionResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/vision_result.h"


#ifndef ACARE_MSGS__MSG__DETAIL__VISION_RESULT__STRUCT_H_
#define ACARE_MSGS__MSG__DETAIL__VISION_RESULT__STRUCT_H_

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
// Member 'zone'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/VisionResult in the package acare_msgs.
typedef struct acare_msgs__msg__VisionResult
{
  bool found;
  rosidl_runtime_c__String tool;
  float x;
  float y;
  float z;
  float confidence;
  rosidl_runtime_c__String zone;
} acare_msgs__msg__VisionResult;

// Struct for a sequence of acare_msgs__msg__VisionResult.
typedef struct acare_msgs__msg__VisionResult__Sequence
{
  acare_msgs__msg__VisionResult * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__msg__VisionResult__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__VISION_RESULT__STRUCT_H_
