// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:msg/AuthResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/auth_result.h"


#ifndef ACARE_MSGS__MSG__DETAIL__AUTH_RESULT__STRUCT_H_
#define ACARE_MSGS__MSG__DETAIL__AUTH_RESULT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'user_id'
// Member 'name'
// Member 'role'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/AuthResult in the package acare_msgs.
typedef struct acare_msgs__msg__AuthResult
{
  rosidl_runtime_c__String user_id;
  rosidl_runtime_c__String name;
  rosidl_runtime_c__String role;
  bool success;
  bool face_verified;
  float face_confidence;
  float voice_confidence;
} acare_msgs__msg__AuthResult;

// Struct for a sequence of acare_msgs__msg__AuthResult.
typedef struct acare_msgs__msg__AuthResult__Sequence
{
  acare_msgs__msg__AuthResult * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__msg__AuthResult__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__MSG__DETAIL__AUTH_RESULT__STRUCT_H_
