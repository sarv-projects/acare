// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:msg/VisionSearchRequest.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/vision_search_request.h"


#ifndef ACARE_MSGS__MSG__DETAIL__VISION_SEARCH_REQUEST__STRUCT_H_
#define ACARE_MSGS__MSG__DETAIL__VISION_SEARCH_REQUEST__STRUCT_H_

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
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/VisionSearchRequest in the package acare_msgs.
typedef struct acare_msgs__msg__VisionSearchRequest
{
  rosidl_runtime_c__String tool;
} acare_msgs__msg__VisionSearchRequest;

// Struct for a sequence of acare_msgs__msg__VisionSearchRequest.
typedef struct acare_msgs__msg__VisionSearchRequest__Sequence
{
  acare_msgs__msg__VisionSearchRequest * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__msg__VisionSearchRequest__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__VISION_SEARCH_REQUEST__STRUCT_H_
